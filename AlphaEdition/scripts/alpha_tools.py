#!/usr/bin/env python3
"""
alpha_tools.py -- checks, renders and packages the OET Alpha Edition
(an unofficial adaptation of the OET Readers' Version).

  python3 alpha_tools.py validate   # compare every AE_*.USFM against its OET-RV source
  python3 alpha_tools.py render     # readable Markdown, both Alpha and Plain
  python3 alpha_tools.py reader     # build reader/alpha_reader.html (self-contained)
  python3 alpha_tools.py all        # validate, then render, then reader

THE SLANG DIAL
  Every slang use is wrapped as   \\zs alpha form|plain form\\zs*
  "Alpha" mode shows the first part; "Plain" mode shows the second (which may be empty).
  Decoder footnotes belong to slang and are hidden in Plain mode.

What `validate` enforces (errors fail the run; warnings need a human look):
  ERROR   chapter/verse/paragraph/poetry/heading marker sequence differs from the OET-RV source
  ERROR   a cross-reference (\\x ... \\xt) is missing, added or changed in a verse
  ERROR   a digit-number in the source verse (e.g. 120,000) is missing from the Alpha verse
  ERROR   a footnote is unbalanced, or does not start with "Decoder:" or "Nerd note:"
  ERROR   a Decoder footnote explains a term that the verse itself doesn't use
  ERROR   a lexicon `avoid` term appears anywhere in the book
  ERROR   a lexicon slang term appears OUTSIDE a \\zs span (no plain fallback = fails the Grandma Test)
  ERROR   a Plain-mode fallback itself contains slang
  ERROR   a \\zs span is malformed
  WARN    a proper name from the OET names table that occurs in the source verse is absent
  WARN    slang density in a chapter is above the threshold (default 3 per 100 words)
  WARN    the Alpha text scores more than 1.5 grade levels harder than the OET-RV (Flesch-Kincaid)

Standard library only. Python 3.8+.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALPHA_ROOT = HERE.parent
REPO_ROOT = ALPHA_ROOT.parent
ALPHA_DIR = ALPHA_ROOT / "translatedTexts" / "AlphaEdition"
SOURCE_DIR = REPO_ROOT / "exportedFiles" / "cleanedUSFM" / "ReadersVersion"
NAMES_TSV = REPO_ROOT / "translatedTexts" / "ReadersVersion" / "OET-RV_names_table.tsv"
LEXICON_TSV = ALPHA_ROOT / "lexicon.tsv"
READABLE_DIR = ALPHA_ROOT / "readable"
READER_DIR = ALPHA_ROOT / "reader"

DENSITY_THRESHOLD = 3.0  # slang terms per 100 words, per chapter
FK_MARGIN = 1.5          # allowed Flesch-Kincaid grade increase over the OET-RV
NON_VERSE_MARKERS = {"s1", "s2", "s3", "s4", "r", "rem", "mt1", "mt2", "is1", "ip", "iot", "io1", "ior"}
# Lexicon words that are also ordinary English; excluded from automatic detection.
AMBIGUOUS_TERMS = {"ate", "cap", "mid"}

FOOT_RE = re.compile(r"\\f\s.*?\\f\*", re.S)
XREF_RE = re.compile(r"\\x\s.*?\\x\*", re.S)
FOOT_PARTS_RE = re.compile(r"\\f\s+\+\s+\\fr\s+(\S+)\s+\\ft\s+(.*?)\\f\*", re.S)
ZS_RE = re.compile(r"\\zs\s+([^|\\]*)\|([^\\]*)\\zs\*")
MARKER_RE = re.compile(r"\\\+?[a-z]+\d?\*?")
LINE_MARKER_RE = re.compile(r"^\\([a-z]+\d?)(?:\s|$)")
NAME_TOKEN_RE = re.compile(r"[A-Za-z\u02bc\u2019'\-]+")


# ----------------------------------------------------------------------------- parsing
def read_lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def split_at_first_chapter(lines):
    for i, line in enumerate(lines):
        if line.startswith("\\c "):
            return lines[:i], lines[i:]
    raise ValueError("no \\c marker found")


def skeleton(body_lines):
    """Sequence of (marker, number) for every line; number only for \\c and \\v."""
    out = []
    for line in body_lines:
        m = LINE_MARKER_RE.match(line)
        if not m:
            out.append(("?", line[:20]))
            continue
        marker = m.group(1)
        num = ""
        if marker in ("c", "v"):
            n = re.match(r"\\[cv]\s+(\S+)", line)
            num = n.group(1) if n else ""
        out.append((marker, num))
    return out


def verses(body_lines):
    """Map (chapter, verse) -> raw text, gathering poetry/paragraph lines that follow a \\v."""
    result, order = {}, []
    ch, vs = None, None
    for line in body_lines:
        m = LINE_MARKER_RE.match(line)
        marker = m.group(1) if m else "?"
        if marker == "c":
            ch = re.match(r"\\c\s+(\S+)", line).group(1)
            vs = None
        elif marker == "v":
            vs = re.match(r"\\v\s+(\S+)", line).group(1)
            key = (ch, vs)
            order.append(key)
            result[key] = re.sub(r"^\\v\s+\S+\s*", "", line)
        elif vs is not None and marker not in NON_VERSE_MARKERS:
            rest = re.sub(r"^\\[a-z]+\d?\s*", "", line)
            if rest.strip():
                result[(ch, vs)] += " " + rest
    return result, order


def xref_list(raw):
    out = []
    for blk in XREF_RE.findall(raw):
        out.append(re.sub(r"^.*?\\xt\s+", "", blk, flags=re.S).replace("\\x*", "").strip())
    return sorted(out)


def footnotes(raw):
    return [(ref, text.strip()) for ref, text in FOOT_PARTS_RE.findall(raw)]


def resolve_zs(text, mode):
    """mode: 'alpha' (slang), 'plain' (fallback) or 'strip' (remove span; detects unwrapped slang)."""
    if mode == "alpha":
        return ZS_RE.sub(lambda m: m.group(1), text)
    if mode == "plain":
        return ZS_RE.sub(lambda m: m.group(2), text)
    return ZS_RE.sub(" ", text)


def plain(raw, mode="alpha"):
    t = FOOT_RE.sub(" ", raw)
    t = XREF_RE.sub(" ", t)
    t = resolve_zs(t, mode)
    t = MARKER_RE.sub("", t)
    return re.sub(r"\s+", " ", t).strip()


def norm_quotes(s):
    return s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')


# ----------------------------------------------------------------------------- readability
def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith("le") and n > 1:
        n -= 1
    return max(1, n)


def fk_grade(text):
    words = re.findall(r"[A-Za-z\u2019']+", text)
    if not words:
        return 0.0
    sentences = max(1, len(re.findall(r"[.!?]+(?:[\s\u201d\"')]|$)", text)))
    syl = sum(syllables(w) for w in words)
    return 0.39 * len(words) / sentences + 11.8 * syl / len(words) - 15.59


# ----------------------------------------------------------------------------- data
def load_names():
    names = set()
    if not NAMES_TSV.exists():
        return names
    with NAMES_TSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            n = (row.get("RVName") or "").strip()
            if len(n) >= 4:
                names.add(n)
    return names


def load_lexicon():
    avoid, use = [], []
    if not LEXICON_TSV.exists():
        return avoid, use
    with LEXICON_TSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            tier = row["tier"].strip()
            for variant in re.split(r"\s*/\s*", row["term"].strip()):
                v = variant.strip().lower()
                if not v or v in AMBIGUOUS_TERMS or v == "no cap":
                    if v == "no cap" and tier in ("use", "use-with-gloss"):
                        use.append(v)
                    continue
                if tier == "avoid":
                    avoid.append(v)
                elif tier in ("use", "use-with-gloss"):
                    use.append(v)
    return avoid, use


def term_regex(term):
    # Allow simple inflections so 'unalive' also catches 'unalived', 'unaliving' etc.
    if term.endswith("e"):
        stem = re.escape(term[:-1]) + r"(?:e|ed|es|ing)"
    else:
        stem = re.escape(term) + r"(?:s|es|ed|ing|ging)?"
    return re.compile(r"(?<![A-Za-z])" + stem + r"(?![A-Za-z])", re.I)


# ----------------------------------------------------------------------------- validate
def validate_pair(alpha_path, source_path, names, avoid, use, threshold):
    errors, warnings, report = [], [], []
    a_lines, s_lines = read_lines(alpha_path), read_lines(source_path)
    _, a_body = split_at_first_chapter(a_lines)
    _, s_body = split_at_first_chapter(s_lines)

    # 1. structure
    a_sk, s_sk = skeleton(a_body), skeleton(s_body)
    if a_sk != s_sk:
        for i, (x, y) in enumerate(zip(a_sk, s_sk)):
            if x != y:
                errors.append(f"structure differs at body line {i + 1}: alpha {x} vs source {y}")
                break
        else:
            errors.append(f"structure length differs: alpha {len(a_sk)} lines vs source {len(s_sk)}")

    a_v, a_order = verses(a_body)
    s_v, _ = verses(s_body)

    n_spans = 0
    # 2-5. per verse
    for key in a_order:
        ch, vs = key
        label = f"{ch}:{vs}"
        if key not in s_v:
            errors.append(f"{label}: verse not in source")
            continue
        a_raw, s_raw = a_v[key], s_v[key]
        if xref_list(a_raw) != xref_list(s_raw):
            errors.append(f"{label}: cross-references differ (alpha {xref_list(a_raw)} vs source {xref_list(s_raw)})")
        a_txt, s_txt = plain(a_raw, "alpha"), plain(s_raw)
        for num in re.findall(r"\d[\d,]*\d|\d", s_txt):
            if num not in a_txt:
                errors.append(f"{label}: number {num} from source is missing")
        a_tokens = set(NAME_TOKEN_RE.findall(a_txt)) | {re.sub(r"[\u2019']s$", "", t) for t in NAME_TOKEN_RE.findall(a_txt)}
        for tok in set(NAME_TOKEN_RE.findall(s_txt)):
            base = re.sub(r"[\u2019']s$", "", tok)
            if base in names and tok[:1].isupper() and base not in a_tokens and tok not in a_tokens:
                warnings.append(f"{label}: name '{base}' appears in source verse but not in alpha verse")
        # footnotes
        if a_raw.count("\\f ") != a_raw.count("\\f*"):
            errors.append(f"{label}: unbalanced footnote markers")
        for ref, text in footnotes(a_raw):
            if not (text.startswith("Decoder:") or text.startswith("Nerd note:")):
                errors.append(f"{label}: footnote must start with 'Decoder:' or 'Nerd note:' (got '{text[:30]}...')")
            if text.startswith("Decoder:"):
                m = re.search(r"\u2018([^\u2019]+)\u2019", text)
                if not m:
                    errors.append(f"{label}: Decoder footnote has no quoted term")
                elif norm_quotes(m.group(1)).lower() not in norm_quotes(a_txt).lower():
                    errors.append(f"{label}: Decoder explains '{m.group(1)}' but the verse doesn't use it")
        # slang-dial span checks
        spans = ZS_RE.findall(a_raw)
        n_spans += len(spans)
        if a_raw.count("\\zs ") != len(spans) or a_raw.count("\\zs*") != len(spans):
            errors.append(f"{label}: malformed \\zs span (need '\\zs alpha|plain\\zs*')")
        for a_form, p_form in spans:
            if not a_form.strip():
                errors.append(f"{label}: \\zs span has an empty Alpha form")
        stripped = norm_quotes(plain(a_raw, "strip"))
        for term in use:
            if term_regex(term).search(stripped):
                errors.append(f"{label}: slang '{term}' is used outside a \\zs span (no plain fallback)")
        plain_txt = norm_quotes(plain(a_raw, "plain"))
        for term in use + avoid:
            if term_regex(term).search(plain_txt):
                errors.append(f"{label}: Plain fallback still contains '{term}'")

    # 6. avoid-list over the whole body (including footnotes and fallbacks)
    whole = norm_quotes("\n".join(a_body))
    for term in avoid:
        if term_regex(term).search(whole):
            errors.append(f"avoid-list term used: '{term}'")

    # 7. density and readability per chapter
    chapters = {}
    for (ch, vs), raw in a_v.items():
        chapters.setdefault(ch, {"alpha": [], "plain": [], "rv": []})
        chapters[ch]["alpha"].append(plain(raw, "alpha"))
        chapters[ch]["plain"].append(plain(raw, "plain"))
        if (ch, vs) in s_v:
            chapters[ch]["rv"].append(plain(s_v[(ch, vs)]))
    slang_total = 0
    all_alpha, all_plain, all_rv = [], [], []
    for ch, d in sorted(chapters.items(), key=lambda kv: int(kv[0])):
        blob = " ".join(d["alpha"])
        words = max(1, len(blob.split()))
        hits = [t for t in use if term_regex(t).search(blob)]
        count = sum(len(term_regex(t).findall(blob)) for t in hits)
        slang_total += count
        density = 100.0 * count / words
        fk_a, fk_p, fk_r = fk_grade(blob), fk_grade(" ".join(d["plain"])), fk_grade(" ".join(d["rv"]))
        all_alpha += d["alpha"]; all_plain += d["plain"]; all_rv += d["rv"]
        report.append(
            f"  ch {ch}: {words} words | slang {count} {sorted(set(hits)) or ''} = {density:.2f}/100w | "
            f"FK grade RV {fk_r:.1f}, Alpha {fk_a:.1f}, Plain {fk_p:.1f}"
        )
        if density > threshold:
            warnings.append(f"ch {ch}: slang density {density:.2f}/100 words is above {threshold}")
    fk = {"rv": fk_grade(" ".join(all_rv)), "alpha": fk_grade(" ".join(all_alpha)), "plain": fk_grade(" ".join(all_plain))}
    if fk["alpha"] > fk["rv"] + FK_MARGIN:
        warnings.append(f"Alpha reads {fk['alpha'] - fk['rv']:.1f} grade levels harder than the OET-RV")
    n_foot = sum(len(footnotes(r)) for r in a_v.values())
    n_dec = sum(1 for r in a_v.values() for _, t in footnotes(r) if t.startswith("Decoder:"))
    report.append(f"  whole book FK grade: RV {fk['rv']:.1f} | Alpha {fk['alpha']:.1f} | Plain {fk['plain']:.1f}")
    report.append(f"  footnotes: {n_foot} ({n_dec} Decoder, {n_foot - n_dec} Nerd note); dial spans: {n_spans}; verses: {len(a_order)}")
    stats = {
        "verses": len(a_order), "footnotes": n_foot, "decoder": n_dec, "nerd": n_foot - n_dec,
        "spans": n_spans, "slang_hits": slang_total, "fk": fk,
        "words_alpha": len(" ".join(all_alpha).split()), "words_rv": len(" ".join(all_rv).split()),
    }
    return errors, warnings, report, stats


def cmd_validate(args, quiet=False):
    names = load_names()
    avoid, use = load_lexicon()
    files = sorted(Path(args.alpha_dir).glob("AE_*.USFM"))
    if not files:
        print("no AE_*.USFM files found", file=sys.stderr)
        return 2, {}
    total_err, all_stats = 0, {}
    for f in files:
        code = f.stem.split("_", 1)[1]
        src = Path(args.source_dir) / f"OET-RV_{code}.USFM"
        print(f"\n== {f.name}  (source: {src.name})")
        if not src.exists():
            print(f"  ERROR: source file {src} not found")
            total_err += 1
            continue
        errs, warns, rep, stats = validate_pair(f, src, names, avoid, use, args.threshold)
        for line in rep:
            print(line)
        for w in warns:
            print(f"  WARN  {w}")
        for e in errs:
            print(f"  ERROR {e}")
        print(f"  -> {len(errs)} error(s), {len(warns)} warning(s)")
        stats.update({"errors": len(errs), "warnings": len(warns)})
        all_stats[code] = stats
        total_err += len(errs)
    print(f"\nTOTAL ERRORS: {total_err}")
    return (1 if total_err else 0), all_stats


# ----------------------------------------------------------------------------- render
def render_file(path, mode="alpha"):
    lines = read_lines(path)
    out, notes, fn_counter = [], [], [0]
    poetry = False

    def inline(text):
        text = resolve_zs(text, mode)

        def foot_sub(m):
            parts = FOOT_PARTS_RE.match(m.group(0))
            ref, ftxt = (parts.group(1), parts.group(2).strip()) if parts else ("", m.group(0))
            label, _, rest = ftxt.partition(":")
            if mode == "plain" and label == "Decoder":
                return ""
            fn_counter[0] += 1
            n = fn_counter[0]
            if label in ("Decoder", "Nerd note"):
                notes.append(f"[^{n}]: **{label}.** {rest.strip()}")
            else:
                notes.append(f"[^{n}]: {ftxt}")
            return f"[^{n}]"

        text = FOOT_RE.sub(foot_sub, text)
        text = XREF_RE.sub(lambda m: " *(cf. " + re.sub(r"^.*?\\xt\s+", "", m.group(0), flags=re.S).replace("\\x*", "").strip().rstrip(".") + ")*", text)
        text = re.sub(r"\\(?:em|bk)\s+(.*?)\\(?:em|bk)\*", r"*\1*", text)
        text = re.sub(r"\\ior\s+(.*?)\\ior\*", r"(\1)", text)
        text = MARKER_RE.sub("", text)
        return re.sub(r"[ \t]+", " ", text).strip()

    def flush_notes():
        if notes:
            out.append("")
            out.extend(notes)
            notes.clear()

    for line in lines:
        m = LINE_MARKER_RE.match(line)
        if not m:
            continue
        marker = m.group(1)
        rest = re.sub(r"^\\[a-z]+\d?\s*", "", line)
        if marker in ("id", "usfm", "ide", "rem", "h", "toc1", "toc2", "toc3"):
            continue
        if marker == "mt2":
            out.append(f"*{inline(rest)}*")
        elif marker == "mt1":
            out.append(f"# {inline(rest)}" + (" (Plain mode)" if mode == "plain" else "") + "\n")
        elif marker == "is1":
            out.append("## Introduction\n")
        elif marker == "ip":
            out.append(inline(rest) + "\n")
        elif marker == "iot":
            out.append(f"**{inline(rest)}**\n")
        elif marker == "io1":
            out.append(f"- {inline(rest)}")
        elif marker == "c":
            flush_notes()
            poetry = False
            out.append(f"\n## Chapter {rest.strip()}\n")
        elif marker == "s1":
            out.append(f"### {inline(rest)}\n")
        elif marker == "s4":
            out.append(f"*{inline(rest)}*\n")
        elif marker == "p":
            poetry = False
            out.append("")
            if rest.strip():
                out.append(inline(rest))
        elif marker == "q1":
            poetry = True
            out.append("")
            if rest.strip():
                out.append("> " + inline(rest))
        elif marker == "v":
            vm = re.match(r"(\S+)\s*(.*)", rest, re.S)
            num, body = vm.group(1), vm.group(2)
            out.append(("> " if poetry else "") + f"<sup>**{num}**</sup> {inline(body)}")
        elif rest.strip():
            out.append(inline(rest))
    flush_notes()
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def cmd_render(args):
    READABLE_DIR.mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(args.alpha_dir).glob("AE_*.USFM")):
        for mode, suffix in (("alpha", ".md"), ("plain", ".plain.md")):
            target = READABLE_DIR / (f.stem + suffix)
            target.write_text(render_file(f, mode), encoding="utf-8")
            print(f"wrote {target}")
    return 0


# ----------------------------------------------------------------------------- reader data
TOKEN_RE = re.compile(r"(\\f\s.*?\\f\*)|(\\x\s.*?\\x\*)|(\\zs\s+[^|\\]*\|[^\\]*\\zs\*)", re.S)


def _clean(text):
    text = re.sub(r"\\(?:em|bk)\s+(.*?)\\(?:em|bk)\*", r"*\1*", text)
    text = MARKER_RE.sub("", text)
    return re.sub(r"[ \t]{2,}", " ", text)


def segments(raw):
    segs, pos = [], 0
    for m in TOKEN_RE.finditer(raw):
        if m.start() > pos:
            segs.append({"t": "text", "s": _clean(raw[pos:m.start()])})
        if m.group(1):
            parts = FOOT_PARTS_RE.match(m.group(1))
            ftxt = parts.group(2).strip() if parts else m.group(1)
            label, _, rest = ftxt.partition(":")
            segs.append({"t": "note", "kind": "decoder" if label == "Decoder" else "nerd", "s": rest.strip()})
        elif m.group(2):
            segs.append({"t": "xref", "s": re.sub(r"^.*?\\xt\s+", "", m.group(2), flags=re.S).replace("\\x*", "").strip().rstrip(".")})
        else:
            zs = ZS_RE.match(m.group(3))
            segs.append({"t": "zs", "a": zs.group(1), "p": zs.group(2)})
        pos = m.end()
    if pos < len(raw):
        segs.append({"t": "text", "s": _clean(raw[pos:])})
    if segs and segs[0]["t"] == "text":
        segs[0]["s"] = segs[0]["s"].lstrip()
    return [s for s in segs if not (s["t"] == "text" and not s["s"])]


def build_book(alpha_path, source_path):
    a_head, a_body = split_at_first_chapter(read_lines(alpha_path))
    s_head, s_body = split_at_first_chapter(read_lines(source_path))
    if skeleton(a_body) != skeleton(s_body):
        raise ValueError(f"{alpha_path.name}: structure differs from source; run validate first")
    book = {"code": alpha_path.stem.split("_", 1)[1].upper(), "title": "", "subtitle": "", "intro": [], "outline": [], "chapters": []}
    for line in a_head:
        m = LINE_MARKER_RE.match(line)
        if not m:
            continue
        mk, rest = m.group(1), re.sub(r"^\\[a-z]+\d?\s*", "", line)
        if mk == "mt1":
            book["title"] = plain(rest)
        elif mk == "mt2":
            book["subtitle"] = plain(rest)
        elif mk == "ip":
            book["intro"].append(_clean(rest))
        elif mk == "io1":
            ref = re.search(r"\\ior\s+(.*?)\\ior\*", rest)
            book["outline"].append({"text": plain(re.sub(r"\\ior.*?\\ior\*", "", rest)), "ref": ref.group(1) if ref else ""})
    chap, pending_h, pending_sub, para, poetry, cur = None, None, None, False, False, None
    for a_line, s_line in zip(a_body, s_body):
        mk = LINE_MARKER_RE.match(a_line).group(1)
        a_rest = re.sub(r"^\\[a-z]+\d?\s*", "", a_line)
        s_rest = re.sub(r"^\\[a-z]+\d?\s*", "", s_line)
        if mk == "c":
            chap = {"n": int(a_rest.strip()), "verses": []}
            book["chapters"].append(chap)
            pending_h = pending_sub = None
            para, poetry, cur = True, False, None
        elif mk == "s1":
            pending_h = {"a": plain(a_rest), "rv": plain(s_rest)}
        elif mk == "s4":
            pending_sub = plain(a_rest)
        elif mk in ("p", "q1"):
            para = True
            poetry = mk == "q1"
            if a_rest.strip() and cur is not None:
                cur["a"].append({"t": "para"})
                cur["a"].extend(segments(a_rest))
                cur["rv"] += "\n" + plain(s_rest)
        elif mk == "v":
            vm = re.match(r"(\S+)\s*(.*)", a_rest, re.S)
            sm = re.match(r"(\S+)\s*(.*)", s_rest, re.S)
            cur = {"n": vm.group(1), "para": para, "poetry": poetry, "a": segments(vm.group(2)), "rv": plain(sm.group(2)), "xrefs": xref_list(vm.group(2))}
            if pending_h:
                cur["h"] = pending_h
            if pending_sub:
                cur["sub"] = pending_sub
            pending_h = pending_sub = None
            para = False
            chap["verses"].append(cur)
    return book


def cmd_reader(args):
    template = READER_DIR / "template.html"
    if not template.exists():
        print(f"missing {template}", file=sys.stderr)
        return 2
    rc, stats = cmd_validate(args)
    if rc:
        print("validation failed; not building the reader", file=sys.stderr)
        return rc
    books = []
    for f in sorted(Path(args.alpha_dir).glob("AE_*.USFM")):
        code = f.stem.split("_", 1)[1]
        books.append(build_book(f, Path(args.source_dir) / f"OET-RV_{code}.USFM"))
    for b in books:
        b["checks"] = stats.get(b["code"].capitalize(), stats.get(b["code"], {}))
    data = {"books": books}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = template.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    target = READER_DIR / "alpha_reader.html"
    target.write_text(html, encoding="utf-8")
    print(f"wrote {target} ({len(html) / 1024:.0f} KB)")
    # Deployable copy for static hosting (Cloudflare Pages: output dir AlphaEdition/site)
    site = READER_DIR.parent / "site"
    site.mkdir(exist_ok=True)
    # Strict-CSP variant (script-src 'self', no external fonts): the one inline
    # script moves to reader.js and the Google Fonts link is dropped (the CSS
    # font stacks already fall back to system fonts).
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    if len(scripts) != 1:
        print(f"expected exactly one inline script, found {len(scripts)}", file=sys.stderr)
        return 2
    strict = html.replace(f"<script>{scripts[0]}</script>", '<script src="reader.js"></script>')
    strict = re.sub(r'\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', "", strict)
    (site / "reader.js").write_text(scripts[0].strip() + "\n", encoding="utf-8")
    (site / "index.html").write_text(strict, encoding="utf-8")
    print(f"wrote {site / 'index.html'} + reader.js (CSP-safe)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["validate", "render", "reader", "all"])
    ap.add_argument("--alpha-dir", default=str(ALPHA_DIR))
    ap.add_argument("--source-dir", default=str(SOURCE_DIR))
    ap.add_argument("--threshold", type=float, default=DENSITY_THRESHOLD)
    args = ap.parse_args()
    if args.command == "validate":
        sys.exit(cmd_validate(args)[0])
    if args.command == "render":
        sys.exit(cmd_render(args))
    if args.command == "reader":
        sys.exit(cmd_reader(args))
    rc = cmd_validate(args)[0]
    if rc:
        sys.exit(rc)
    cmd_render(args)
    sys.exit(cmd_reader(args))


if __name__ == "__main__":
    main()
