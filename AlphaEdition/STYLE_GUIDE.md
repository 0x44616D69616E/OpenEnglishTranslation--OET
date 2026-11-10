# OET Alpha Edition: style guide

*An unofficial, AI-assisted register adaptation of the OET Readers’ Version, written for Gen Alpha and designed so that a parent, a teacher, or a grandparent can read it without a translator.*

**Brief (from the request):** Gen Alpha, understandable across generations, intellectual but relatable, and funny.

Gen Alpha is commonly defined as people born from about 2010 onward. That convention is general knowledge; none of the sources I fetched pinned it down.

---

## 0. Scope and translation philosophy (the two big decisions)

**Does this remake the Literal Version, the Readers' Version, or both?**
Neither, strictly. It is a *register layer on top of the Readers' Version (OET-RV)*. The OET Literal Version (OET-LV) is left untouched and is the intended companion: the OET's own design pairs a very literal version with a more dynamic one and says they are meant to be used together and never alone. Slang inside a word-for-word gloss would destroy the one thing the LV is for, so the generational work does not go there. The focus is the *Gen* aspect: how the same meaning sounds to a Gen Alpha reader and stays readable to everyone else.

**What translation style is it?**
**Thought-for-thought (dynamic) at the sentence level, with hard fidelity limits.** The RV is already dynamic by design (natural English first, accuracy checked afterwards), so this edition does not drift further from the original wording than the RV does. What changes is *voice*, not content:

| Locked (validator-enforced) | Free (the Alpha layer) |
|---|---|
| events, who says what, names, numbers, cross-references, verse/paragraph/poetry structure | sentence rhythm, idiom, word choice, narrator asides, headings, introductions |
| meaning of divine speech, prayers and laments | footnotes (*Decoder*, *Nerd note*) where the freer reading or the joke lives |

When a freer reading would change *what the text claims*, it goes in a footnote, never into the verse.

**Open decisions you may want to change** (answers shape the next books):
1. Keep it RV-only, or also add an Alpha layer for the Literal Version (for example Decoder-style notes aligned to the LV's word table)?
2. Hold the current "close to the RV" setting, or push freer and more idiomatic (more thought-for-thought, more risk)?
3. Slang dial default: the pilots sit at 0.2–0.8 slang uses per 100 words. Higher, or stay light?
4. Which books next (narrative such as Ruth and Mark take slang best; law and genealogies least)?

## 1. What the research says, and what we did about it

| # | Finding | Source | Design consequence |
|---|---|---|---|
| 1 | Social-media algorithms are a major engine of how Gen Alpha language changes: they amplify words already trending, creators adopt them to stay relevant, and the cycle repeats. Middle schoolers lead the change. | Adam Aleksic on [Science Friday](https://www.sciencefriday.com/segments/what-is-algospeak-gen-alpha/) | Slang is volatile by construction. It lives in a swappable lexicon, not in the grammar of the text. |
| 2 | Once adults adopt a slang term, younger people tend to drop it, so lifespans keep shrinking. | Aleksic, same source | The introduction says out loud that the slang will age. Every slang use needs a plain-word fallback. |
| 3 | A lot of Gen Alpha slang is *deliberately* meaningless. "67" is a shouted interjection with no fixed definition, picked as Dictionary.com's 2025 Word of the Year. Its value is belonging, not meaning. | [CBS News](https://www.cbsnews.com/amp/news/dictionary-67-2025-word-of-the-year-meaning) | A translation exists to carry meaning, so meaningless slang is on the **avoid** list. We *describe* brainrot (in notes); we don't write in it. |
| 4 | "Brain rot" names three things at once: the absurd content, the scattered focus it leaves, and a proud, self-mocking identity. The humor is intentionally nonsensical and works as escapism. Harm seems to come from dosage. (Secondary source; it relays attention research from Gloria Mark, Stanford, and Anna Lembke.) | [Science of People](https://www.scienceofpeople.com/what-is-brain-rot/) | Humor here is self-aware and absurd in *tone*, but the content stays coherent. |
| 5 | Dictionary.com's 2026 Word of the Year is **"maxxing"** (doing something to the fullest); its shortlist included "unc." | [Euronews](https://www.euronews.com/2026/10/26/dictionarycoms-reveals-2026-word-of-the-year-and-its-a-depressing-one) | Both are in the lexicon as `use`, in their neutral senses only. |
| 6 | The most-searched Gen Alpha terms of 2026 (Google Trends, Jan–Aug 2026) include 6-7, chud, rizz, cap, mogging, bop, larping, aura, sigma, crash out. Mental Floss flags chud, bop, sigma, huzz and foid as contested or harmful, and says "foid" is a cause for concern. | [Mental Floss](https://www.mentalfloss.com/language/slang/top-gen-alpha-slang-2026), [Euronews](https://www.euronews.com/2026/09/28/from-chud-to-bop-most-searched-gen-alpha-slang-terms-of-2026-so-far-revealed) | Flagged terms are on the **avoid** list and the validator fails any book that uses them. |
| 7 | Moderation-dodging euphemisms ("unalive") spread from platforms into everyday speech, even student essays. | Aleksic (Science Friday) | Scripture has killings, executions and a prophet asking to die. Euphemism would trivialise them. **Avoid-list; use plain words.** |
| 8 | Much Gen Z/Alpha slang traces to African American English. Linguists quoted by NBC describe AAVE as a fully rule-governed dialect and warn that dropping the origin erases history. | [NBC News](https://www.nbcnewyork.com/news/national-international/appreciation-appropriation-black-culture-shaping-gen-z-slang/6485385/) (quoting Jamaal Muwwakkil, Sonja Lanehart, Minnie Annan) | Vocabulary only, never imitated dialect grammar. Origins are noted in `lexicon.tsv`. |
| 9 | Gen Alpha inherits Gen Z conventions. Text tone is carried by punctuation and line breaks (a full stop can read as cold); discourse markers like "like" and "literally" do real pragmatic work (hedging, quoting, softening); "and stuff"-type extenders signal vagueness or solidarity, and "and idk" signals vulnerability. | [A Little Bit Human](https://alittlebithuman.com/gen-z-paralinguistics-and-language/), [UCLA Languaged Life](https://languagedlife.ucla.edu/sociolinguistics/gen-z-slang-and-stuff), [AUC Caravan](https://www.auccaravan.com/filler-words-gen-z-didnt-ruin-english-you-like-just-dont-get-it/) | Standard punctuation stays (USFM and readability). One emphatic exclamation per scene at most ("WHAT did you do?!"). Discourse markers are used sparingly ("honestly", "okay, explain"). |
| 10 | Young people's online humor is heavily self-deprecating and ironic, and does coping, solidarity and identity work. (Small qualitative blog-post study; its percentages are illustrative only.) | [UCLA Languaged Life](https://languagedlife.ucla.edu/?p=3523), [InsuranceNewsNet / Clarkson](https://insurancenewsnet.com/oarticle/why-gen-z-turns-everything-even-murder-into-a-joke) | Humor aims at human foibles (Yonah’s sulking, Paulos’s polite pressure), which is where the source text already points. |
| 11 | Earlier "Gen Z Bible" efforts are criticised for sacrificing accuracy, distracting from meaning, and relying on AI plus a public-domain base text without Hebrew/Greek training. | [GotQuestions summary](https://www.gotquestions.org/Gen-Z-Bible-translations.html) (one critic's view of one project) | Mitigations below: base on OET-RV, validate structure, put jokes outside the text, check footnote claims against OET's original-language tables, and disclose the AI involvement. |

**Source quality.** Several of these are news or blog summaries, and the humor study is small and qualitative. One relevant NBC piece on parents and "brainrot" language could not be fetched (blocked), so nothing here relies on it. Treat the findings as informed direction, not as established linguistics.

---

## 2. Design principles

1. **Fidelity first.** Same events, same names, same numbers, same cross-references as the OET-RV, verse for verse. The validator enforces the checkable parts.
2. **The Grandma Test.** Every slang word must be guessable from its sentence, or carry a *Decoder* footnote. If neither is true, cut the word.
3. **Jokes live in the voice, not the facts.** Humor goes in word choice, narrator asides and footnotes. We never add an event or a claim to make a joke.
4. **No jokes at the expense of God, victims or pain.** Divine speech, prayers, laments, deaths, slavery and Yonah’s death-wish (4:3, 4:8) are rendered plainly. Humor targets human foibles.
5. **Intellectual means checkable.** *Nerd notes* are short, hedged where scholars disagree, and (for Hebrew/Greek claims) verified against the OET tables. See §5.
6. **Two footnote labels, always.** *Decoder:* explains slang the verse actually uses. *Nerd note:* gives background. Anything else fails validation.
7. **Vocabulary, not dialect.** We borrow words, not grammar, and we credit origins.
8. **Plain words for hard things.** No euphemism for death, killing or suicide.
9. **Slang is a dial, not a coat of paint.** Density per genre is in §3; the validator reports it per chapter.
10. **Say the quiet part.** Each book’s introduction tells the reader the slang will age, and why.

### The slang dial (mechanical, not a promise)

Every slang use is wrapped in the USFM span `\zs alpha form|plain form\zs*`. The reader and the Markdown renderer show either side, so the same file gives an Alpha text and a Plain text. `validate` fails any book where a lexicon slang term appears outside a span, where a Plain fallback itself contains slang, or where a span is malformed. That turns the Grandma Test (principle 2) into a check the computer can run.

### Readability

`validate` reports Flesch–Kincaid grade per chapter for the OET-RV, the Alpha text and the Plain text, and warns if Alpha is more than 1.5 grades harder than the RV. Current pilot results: Jonah RV 7.2 / Alpha 5.8 / Plain 5.8; Philemon RV 9.7 / Alpha 8.5 / Plain 8.5. Treat these as a direction only: the formula is crude (simple sentence splitting, dialogue and names distort it), and it says nothing about humor or accuracy.

## 3. Density dial by genre

| Genre | Slang | Humor | Notes |
|---|---|---|---|
| Narrative (Jonah, Ruth, Mark) | light–medium | narrator wit, deadpan, anticlimax | Best home for gaming idioms (respawn, locked in). |
| Divine speech | none | none | Plain, direct, warm. |
| Prayer, psalm, lament | none | none | Confessional plain speech. |
| Letters (Philemon) | light | affectionate, wry | Lean on rhetoric: Paulos is funny on purpose. |
| Law, genealogy, ritual | minimal | in footnotes only | Let structure be the joke (“Nerd note: yes, everyone is named.”). |
| Wisdom, proverbs | light–medium | one-liners | Revisit `glazing` for flattery proverbs. |
| Prophetic judgment, apocalyptic | none–light | none | Menace shouldn’t read like a meme. |

Current pilot densities are **0.2–0.8 slang hits per 100 words**. That is deliberately light: it keeps the text readable across generations and leaves the humor to the narrator voice and footnotes. Turning it up is a one-line request.

## 4. What changed from the OET-RV, and what was lost

- **Kept:** all chapter/verse/paragraph/poetry/heading structure; OET’s names (Yonah, Yafo, Filemon, Paulos…); `\nd` markup for divine names; cross-references; numbers; the OET’s own “(Jonah)”-style glosses.
- **Dropped:** the word-link markers (`¦370574`) and most `\add` markup, because the OET’s alignment to the Literal Version doesn’t survive a rewrite. This is why the **source base is the cleaned USFM export** (`exportedFiles/cleanedUSFM/ReadersVersion/`), which already omits those links. The OET’s transparent tracking of added words is therefore **not** preserved here.
- **Added:** introductions rewritten in the new voice; section headings rewritten; *Decoder* and *Nerd note* footnotes; a few narrator asides.
- **Not done:** no new translation from Hebrew or Greek. This is a register adaptation of an English translation. For doctrine, study or quotation, use the OET-RV and Literal Version.
- **Unresolved source text:** Philemon 6 carries a translator’s query (“[WHAT DOES THAT MEAN???]”) in the OET-RV draft. This edition renders one reasonable reading and says so in a footnote.

## 5. Footnote claims and how they were checked

Checked against the OET’s own original-language data (`translatedTexts/ReadersVersion/OET-LV_OT_word_table.tsv` and `OET-LV_NT_word_table.tsv`):

| Claim (footnote) | Evidence in OET data |
|---|---|
| Yonah’s whole sermon is five Hebrew words; the last can mean “overthrown” (Jonah 3:4) | `JNA_3:4w10`–`w14` (five words; last glossed “overthrown”) |
| The “fear” root recurs in 1:5, 1:9, 1:10 and 1:16 | `JNA_1:5w1`, `1:10w1`, `1:16w1` (Strong’s 3372); `JNA_1:9w10` (3373, “fearing”) |
| “Huge fish,” not “whale” (1:17) | `JNA_2:1w3`–`w4` (Hebrew numbering for English 1:17): *dāg gādōl* |
| The only “joy/gladness” in the book is 4:6 | Only `JNA_4:6w15` and `w19` carry that root in the whole book |
| Exodus 34:6 echo (4:2) | The OET-RV itself cross-references Exo 34:6 |
| Onesimos pun: “useless/useful” (Phm 11) | `PHM_1:11w4` ἄχρηστον “useless”; `PHM_1:11w11` εὔχρηστον “useful” |
| “You all” in Phm 3 and 25; letter also addressed to the house assembly (v2) | `PHM_1:3w2`, `PHM_1:25w11` (“you_all”); OET-RV verse 2 text |
| Paulos calls himself an “older man” (Phm 9) | `PHM_1:9w11` πρεσβύτης, “older_man” |

**Not verifiable from the OET data (general knowledge, hedged in the text):** that “Onesimos” carries the sense “useful” as a name; Tarshish’s likely location (Spain as a guess); Nineveh lying east of Israel; Philemon being Paulos’s shortest letter; the name for the rhetorical figure *paralipsis*; Roman law treating slaves as property; the Greek “sea monster” word behind “whale”; the scholarly debate over whether Philemon implies freeing Onesimos. These are standard claims but should be confirmed by someone with the relevant expertise before print.

## 6. Adding a new book

1. Copy `exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_Xyz.USFM` to `translatedTexts/AlphaEdition/AE_Xyz.USFM`.
2. Rewrite verse by verse. Keep every `\c`, `\v`, `\p`, `\q1` and `\s` line, and every `\x` cross-reference.
3. Wrap every slang use as `\zs alpha|plain\zs*`. Add footnotes (`\f + \fr C:V \ft Decoder: …\f*` or `Nerd note: …`).
4. Run `python3 AlphaEdition/scripts/alpha_tools.py validate`. Fix every error; read every warning.
5. Run `python3 AlphaEdition/scripts/alpha_tools.py all` to validate, write the Markdown copies (Alpha and Plain) and rebuild `reader/alpha_reader.html`.
6. Have a human reader who knows the book read it against the OET-RV before anyone publishes it.

## 7. Shelf life

Because slang dies fast, `lexicon.tsv` is the only place slang policy lives. To refresh the edition, change terms there, re-run `validate`, and revise the affected verses. Terms marked `author judgment` in the lexicon’s `basis` column were not confirmed in the sources I fetched and should be re-verified before the next release.
