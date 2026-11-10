# OET Alpha Edition (unofficial)

A reading-register adaptation of the **Open English Translation Readers’ Version (OET-RV)** for Gen Alpha: intellectual but relatable, funny without being at God’s expense, and readable by people of any age.

**Status: pilot.** Two books are done: **Jonah** (narrative and poetry) and **Philemon** (letter). The rest of the Bible is not adapted yet.

## Scope in one paragraph

This is a **register layer on the Readers’ Version**, not a remake of the Literal Version (which stays untouched as the companion the OET intends). Style is **thought-for-thought**, as dynamic as the RV already is and no more, with names, numbers, cross-references and structure locked and checked by a validator. Freer readings and jokes go in footnotes. Details and the open decisions are in `STYLE_GUIDE.md` §0.

## What’s here

| Path | What it is |
|---|---|
| `translatedTexts/AlphaEdition/AE_Jon.USFM`, `AE_Phm.USFM` | The adapted books (USFM, same structure as the OET-RV) |
| `readable/AE_*.md`, `AE_*.plain.md` | Markdown with footnotes: Alpha wording, and Plain wording (slang swapped back out) |
| `reader/alpha_reader.html` | Self-contained interactive reader: Alpha / Plain / side-by-side with the OET-RV, tap-open notes, slang you can flip. Built from `reader/template.html` |
| `STYLE_GUIDE.md` | The research, the design rules, the genre dial, how footnote claims were checked |
| `lexicon.tsv` | Slang policy: what’s allowed, what’s banned, where each term comes from |
| `scripts/alpha_tools.py` | `validate` (checks each book against its OET-RV source) and `render` (USFM → Markdown) |

## How it reads

- **Decoder** footnotes explain slang the verse actually uses (cooked, locked in, crashing out, aura, respawn, unc).
- **Nerd notes** give checkable background (Hebrew word counts, the Onesimos pun, the book of Jonah ending on a question).
- Divine speech, prayers, laments and the grim moments are plain. The humor is in the narrator’s voice, the word choice, and the footnotes.

## Run the checks

```
python3 AlphaEdition/scripts/alpha_tools.py validate   # checks only
python3 AlphaEdition/scripts/alpha_tools.py all        # validate, render Markdown, rebuild the reader  (also writes site/index.html for hosting)
```

Python 3.8+, standard library only. `validate` fails on any change to chapter/verse/paragraph structure, cross-references or digit numbers, on malformed footnotes, on any banned slang term, and on any slang that lacks a plain-word fallback (`\zs alpha|plain\zs*`). It also reports Flesch–Kincaid readability for the OET-RV, Alpha and Plain text.

## Attribution and licence

- Based on the **Open English Translation Readers’ Version** (OET-RV v0.4.2 for Jonah, v0.2.0 for Philemon), © 2010–2026 Robert Hunt / [Freely-Given.org](https://Freely-Given.org), licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- **Changes made:** register adaptation into Gen Alpha-aware English; rewritten introductions and headings; added footnotes; simplified markup (see `STYLE_GUIDE.md` §4).
- This adaptation is licensed **CC BY-SA 4.0** under the same terms. `scripts/alpha_tools.py` is original to this edition; the OET’s own scripts are GPL 3.0 or later, and nothing here copies them.
- **Not endorsed by, or affiliated with, the OET project.** The OET README asks forks to rename themselves if they change the text, which is why this carries its own name.
- Adapter credit: *(add your name or handle here)*.

## Read this before sharing it

- **AI-assisted.** The OET-RV states that it is hand-made without AI help. This edition is not, and says so in every file header.
- **A reading aid, not a study text.** No new translation from Hebrew or Greek was done. For study, teaching or quoting, use the OET-RV and Literal Version.
- **Footnotes are unreviewed by a specialist.** Hebrew and Greek claims were checked against the OET word tables (see `STYLE_GUIDE.md` §5); several background claims rest on general knowledge and are listed there. Have a qualified reader check them before anything is printed.
- **Slang will date.** The introductions say so on purpose.
