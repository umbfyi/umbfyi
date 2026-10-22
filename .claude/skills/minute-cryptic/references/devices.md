# Cryptic devices and indicators

Every clue = definition (at the start or end) + wordplay that independently produces the same answer. Read the clue's surface as a normal sentence; it should make sense on its own.

## Anagram
Rearrange the letters of the fodder. Fodder must appear literally in the clue.
Indicators: confused, mixed, broken, wild, crazy, reworked, scrambled, odd, novel, shuffled, ruined, cooked, sorted, refactored, deployed badly, buggy, corrupted, hacked, minified, compiled, rebuilt, debugged, rebased, migrated, hotfixed
Example: Confused cobra, um, becomes friendly CMS (7) = UMBRACO

## Hidden word
The answer is spelled out consecutively inside the clue, ideally across word boundaries.
Indicators: some, part of, in, within, held by, inside, a bit of, partially, contains
Example: Some urn u get delivers packages (5) = NUGET (surface is weak; aim for better)

## Reversal
Clue word(s) read backwards. Across-clue indicators: back, returned, reversed, retreating, going west, rolled back, reverted, undone, popped (as in a stack).
Example: Stressed, returned for afters (8) = DESSERTS

## Hidden reversal
A hidden word that also reads backwards. Combine both indicators: "some returned", "partly back".

## Charade
Parts placed side by side. Each part is a word, an abbreviation, or a synonym. Only use well-known abbreviations (N/S/E/W, L for learner, I for one, O for ring, CE, PR, UI, etc.) and the verifier will flag every non-literal part for you to sanity-check.
Linkers: with, and, by, after (B after A means A then B), before.

### Tech abbreviations this audience knows
Fair for UMB.FYI readers, still flagged by the verifier so you double-check each one:
- API (interface), UI (front end), UX (user experience), CMS (content system), DB (database)
- PR (pull request), CI (build pipeline), QA (testing), IT (tech department), AI (machine smarts)
- JS (JavaScript), TS (TypeScript), CSS (styles), HTML (markup), SQL (query language), URL (web address)
- OS (system), PC (computer), VM (virtual machine), IP (address), KB (kilobyte), MB (megabyte)
- DEV (developer), REPO (repository), APP (application), BUG (defect), LOG (record)
Avoid niche ones (DI, ORM, SPA) unless the surface makes them obvious.

### File extensions
A sneaky source of short parts: name a file type and use its extension. The surface reads as a file, a script or a picture; the wordplay takes the letters. Still flagged by the verifier, so check each one is well known.
- Code: CS (C# file), TS (TypeScript file), JS (script), PY (Python file), RB (Ruby file), GO (Go file), RS (Rust file), PHP, SQL, SH (shell script)
- Web and data: CSS (stylesheet), HTML or HTM (page), JSON, XML, YML (config), CSV (spreadsheet), MD (readme, Markdown)
- Built and binary: DLL (library), EXE (program), ZIP (archive), BAK (backup), TMP (temp file), LOG
- Media and docs: PNG, GIF, JPG (picture), SVG (vector), PDF, DOC (Word file), TXT (text file)
Indicator-style phrasing helps solvers: "C# file" for CS, "the readme's type" for MD, "picture format" for GIF.
Double meanings make the best misdirection: MD looks like a doctor, DOC like a doctor too, LOG like timber, GO like leave, BAK like back.

### Programming languages
Language names are short, well known to this audience, and many already mean something else. Use them as charade parts, double definitions or answers. Still flagged by the verifier, so check each one is well known.
- One letter: C, R, D. These collide with classic abbreviations (C = about or 100, R = river or king, D = 500), so a clue can say "about" and mean the language, or "language" and mean the letter.
- Short names: ASP (ASP.NET), PHP, VB (Visual Basic), ADA, LUA, LISP, GO, ELM, F# (gives F), C# (gives C, or CS as its file type)
- Names with a second meaning, ideal for misdirection and double definitions:
  - ASP (snake), PYTHON (snake), JAVA (coffee, island), RUBY (gem, red), RUST (corrosion), SWIFT (bird, fast)
  - DART (small missile), ELM (tree), GO (leave, a turn), BASIC (simple), KOTLIN (island)
Two-way pull: "snake" can give ASP or PYTHON in the wordplay, and "language" can give C, R, GO or ASP. Lean on the one the surface hides.
Example: Snake language? (3) = ASP, a double definition.

### More dev letter sources
Short parts this audience will spot once they think of them. All still flagged by the verifier.
- HTML tags: B (bold), I (italic), U (underline), P (paragraph), A (link, anchor), EM (emphasis), LI (list item), BR (line break), HR (rule), UL, OL (lists), TD (cell), TR (row). "Bold" for B reads like plain English, which is the point.
- Nothing: NULL, NIL, VOID, ZERO, as well as the classic O. Binary fits too: "one" gives I, "zero" gives O.
- Logic: OR, AND, NOT, XOR. OR is also the classic crossword "gold", so it pulls two ways.
- Keyboard keys: ESC (escape), DEL (delete), ALT, TAB, END, HOME, CTRL (control), SHIFT, ENTER.
- Version: V, which is also 5 in Roman numerals.
- Sizes: BIT, KB, MB, GB, TB. MB is also a doctor and TB an illness, good misdirection.

### Classic crossword abbreviations
Standard in any cryptic, so solvers expect them:
- Directions: N, S, E, W; R (right), L (left, learner)
- Roman numerals: I (one), V (five), X (ten, kiss), L (fifty), C (hundred, about), D (five hundred), M (thousand)
- O (ring, love, zero, nothing, egg)
- People and titles: DR, MD, GP (doctor), ST (saint), K or R (king), ER (queen), MR, MP (politician), PA (assistant), REV (vicar)
- Places and things: ST or RD (street, road), R (river), CE (church), CH (church), T (time), A (one, article), AN (article)
- Musical notes: DO, RE, MI, FA, SO or SOL, LA, TI
- C (about, from circa), RE (about, concerning), CA (about)

## Double definition
Two definitions of the same answer, one at each end, with at most one short link word between (and, or, is, for, as, gives, makes, becomes, of, with, in, to, from, but). No indicator and no fodder.
This is the natural home for double-life words: CACHE (hoard / fast memory), BRANCH (limb / parallel work), COMMIT (pledge / save changes), FORK (cutlery / copy a repo), PATCH (repair / mend fabric), TOKEN (coin / login proof), MERGE (combine / blend lanes).
Make the two halves read as one sentence, so the split isn't obvious.
Example: Hoard fast memory (5) = CACHE
Device name: `double_definition`, with the second definition in `definition2`. In the CMS fields, both go in `definition` as "first / second" and `fodder` stays blank. The verifier checks the length and placement, but always flags both meanings for a human check.

## Container
One part goes inside another. Indicators: in, inside, holding, around, swallowing, nursing, embracing, about.

## First letters (initials)
Take the first letter of each word in a run of clue words. Verified fully by code. The span must be consecutive words, with no skipped words.
Indicators: initially, at first, leaders of, heads of, starts of, opening, firstly, primarily, first in line
Example: Initially developers enjoy breaking useless gadgets? Fix (5) = DEBUG
Device name: `initials`

## Dropping letters (deletion)
Take a word and remove letters. Either remove by position, or remove specific letters the clue names.
- First letter (`drop: "first"`): headless, beheaded, topless, leaderless, losing its head, not starting
- Last letter (`drop: "last"`): endless, curtailed, cut short, unfinished, almost, mostly, nearly
- Both ends (`drop: "ends"`): edgeless, trimmed, peeled, shelled, unwrapped, stripped
- Middle letter (`drop: "middle"`, two letters for even-length words): heartless, gutted, disheartened, cored
- Named letters (`drop: {"text", "yields"}`): without, no, losing, dropping, minus, missing, leaving out, deleted, removed, ignoring, stripped of
Example: Headless anode is part of a tree (4) = NODE
Example: Fast store's cachet, no time (5) = CACHE (T for time is standard)
Device name: `deletion`. The word being cut down may be a synonym (`yields` differs from `text`); the verifier flags it so you can check it's fair.

## Two devices
A charade or container where one part has its own device. Max two devices per clue: the charade/container itself plus one part.
In the JSON, give that part `"device"` (anagram, reversal, hidden, initials or deletion) and its own `"indicator"`; a deletion part also needs `"drop"` (first, last, ends or middle). The verifier then checks the part's letters from its literal text.
Any part that uses wordplay must declare its device. Don't hide a second device as a "synonym" part; the verifier would only warn, not check it.
Examples:
- No Ed, returning, finds part of a tree (4) = NODE: NO + reversal of ED
- Container with an anagram inside: the outer part holds a shuffled inner part
Not supported: a device applied to a synonym (e.g. "headless snake" = ADDER minus A). Parts with a device work on their literal clue text only.

## Misdirection
Pick clue words with a second meaning that pulls the solver the wrong way. Crosswords use "flower" for a river and "number" for an anaesthetic. Tech has plenty of its own: branch, fork, commit, patch, push, pull, stack, heap, shell, bug, cookie, cache, token, port, release. Use the surface to suggest one sense and the wordplay to need the other.

## Fairness rules
- One definition, one wordplay; no padding words beyond short link words (is, gives, for, from, makes, becomes, in).
- The definition must be an accurate definition of the answer (part of speech too).
- Indicator must make grammatical sense with its fodder.
- Don't use the answer itself (or an obvious form of it) in the clue.
