---
name: minute-cryptic
description: Write and mechanically verify single "minute cryptic" style cryptic crossword clues themed on Umbraco, .NET, web tech and coding, e.g. for a weekly puzzle slot in the UMB.FYI Umbraco community newsletter. Use whenever the user asks for a cryptic clue, minute cryptic, newsletter puzzle, wordplay clue, or wants this week's puzzle, even if they don't say "cryptic". Also use when the user gives a word and asks to "clue it".
---

# Minute Cryptic

Produces one publishable cryptic clue plus hints and an explained answer. Language models are poor at letter-level wordplay (they see tokens, not letters), so every candidate clue goes through `scripts/verify_clue.py` before the user sees it. Never present a clue that hasn't passed the verifier.

## Workflow

1. **Pick the answer.** Use the user's word if given. Otherwise read `references/wordbank.md` and propose 3 answers an Umbraco developer would know: one Umbraco-specific term, one wider tech/coding term, and one everyday word with a tech double life (CACHE, BRANCH, MERGE, TOKEN). Double-life words are the sweet spot: they clue as easily as ordinary English but still land with this audience. Any of the three can be a phrase instead of a single word (PULL REQUEST, I REMEMBER BEING DIRTY); include a phrase in most sets of suggestions. Phrases give anagrams more letters to play with and long hidden spans. Avoid repeating recent answers if the user mentions them. Ask the user to choose if they're around; otherwise pick one.

2. **Plan the theme.** The whole clue should feel like it belongs to the Umbraco/dev world, not just the answer:
   - **Definition:** prefer the tech sense of the answer ("version control step" for COMMIT, "fast store" for CACHE). It must still be accurate; a developer reading the answer should nod, not wince.
   - **Surface:** aim for a sentence a developer might actually say: a standup, a code review, a failed deploy, Codegarden, a Friday release.
   - **Fodder and parts:** tech abbreviations from `references/devices.md` are fair game for this audience (CMS, API, UI, PR, DB).

3. **Plan devices.** Read `references/devices.md`. For the answer, look for workable wordplay: anagram fodder that forms a natural phrase, a hidden span across real words, a reversal, first letters of a natural phrase, a word with letters dropped, or a charade of standard abbreviations. Prefer anagrams, hidden words and first letters; they verify fully by code. For a double-life word, try a double definition too: it's the most natural clue for CACHE or BRANCH, though its meanings need your judgement rather than the verifier's. File extensions (CS, TS, MD, GIF) make sneaky charade parts for this audience. A clue may use up to two devices: a charade or container where one part has its own device (see "Two devices" in `references/devices.md`). The readers are mostly developers, so harder two-device clues are welcome; aim for roughly a third of candidates to use two.

4. **Draft 6+ candidates** across at least two devices. Write each as a JSON object (schema in the script's docstring) into `candidates.json`. Aim for a smooth surface reading that sounds like a plausible sentence, ideally with a wink at the Umbraco/dev world.

5. **Verify.** Run:
   ```bash
   python scripts/verify_clue.py candidates.json
   ```
   Drop every FAIL. Do not "fix" a failing clue by adjusting the JSON to match; rewrite the clue and re-verify. For each warning, decide honestly whether the abbreviation or synonym is standard enough for a solver; drop it if not.

6. **Judge the survivors** on: surface reads naturally and fits the dev world; definition is accurate; no padding; difficulty suits a quick puzzle (solvable in a few minutes). Pick the best 3.

7. **Present** the top 3 to the user using the output format below, with your recommendation first. The user chooses; it's going into a public newsletter, so it needs their approval before publishing.

## Output format

For each shortlisted clue:

```markdown
### 🧩 Minute Cryptic
**<clue> (<enumeration>)**

<details><summary>Show definition</summary><definition words, exactly as in the clue></details>
<details><summary>Show indicator</summary><indicator words> (<what it signals, e.g. "an anagram">)</details>
<details><summary>Show fodder</summary><the words the wordplay works on></details>
<details><summary>Answer</summary>**<ANSWER>**: <one-line explanation, e.g. "an anagram (confused) of COBRA + UM, defined as friendly CMS"></details>
```

Solvers reveal hints one at a time, from least to most help. Take each hint straight from the verified JSON (`definition`, `indicator`, `fodder`) so hints can never disagree with the checked clue. For a charade, which has no indicator, use "No indicator: the parts sit side by side" and list each part's clue words as the fodder. For a container, list the outer and inner words as the fodder. For a deletion, give the word being cut down, plus the named letters' clue words if `drop` is an object. For a double definition, give both definitions as the definition hint, use "No indicator: both halves are definitions", and "No fodder: there's no wordplay" for the fodder. For a two-device clue, list both indicators and say what each signals (e.g. "holding (one part inside another) / wild (an anagram)"), and list the fodder in clue order, separated by " / ".

### CMS fields

After the user picks a clue, also give it as a copy-paste block for the Umbraco "Minute Cryptic" element type:

```
clue:         <clue without the enumeration>
enumeration:  <e.g. 5 or 1,8,5,5>
definition:   <definition words; for a double definition, both, in clue order: "Hoard / fast memory">
indicator:    <indicator words, or blank for a plain charade; two-device clues: "holding / wild">
device:       <anagram | hidden | reversal | hidden reversal | charade | container | first letters | dropped letters | double definition; two-device clues: "container / anagram">
fodder:       <fodder words, or blank for a double definition>
answer:       <ANSWER>
explanation:  <one-line explanation>
```

### Past puzzles

Before picking answers in step 1, check `https://umb.fyi/puzzles` for answers already used and don't reuse them. Each past puzzle's answer is in the page HTML, in the hidden answer box (the `<p>` with `data-part="answer"`), as the bold word before the explanation.

This skill only writes and verifies clues. It never updates the site or the newsletter; the `weekly-cryptic` skill handles that.

When `weekly-cryptic` (or another skill) called this one, finish by handing back the chosen clue's CMS fields block and stop. The calling skill carries on from there.

## Example

Answer: UMBRACO
```json
{"clue": "Confused cobra, um, becomes friendly CMS (7)", "answer": "UMBRACO",
 "definition": "friendly CMS", "device": "anagram", "indicator": "Confused",
 "fodder": ["cobra", "um"]}
```
Verifier: PASS. Surface reads as a slightly silly sentence, definition plays on Umbraco's "friendly CMS" tagline.

## Changing the verifier

After any edit to `scripts/verify_clue.py`, run `python3 tests/test_verify_clue.py` and keep it green. Add a passing and a failing case to the tests for every new device or rule.
