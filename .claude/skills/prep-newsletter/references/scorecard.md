# Prep scorecard

How often Matt takes what prep proposes, step by step. This is how we decide which steps ask him. Newest issue first. This repo is public: counts and short notes only, never private data (tips' submitter details, emails, keys).

## Which steps ask Matt

Matt, 25-11-2026: only ask what needs his approval. So in phone mode (the scheduled runs) every step runs by itself, and he's only asked about things the run isn't sure of. The exception is the `Ask:` line below.

- **Running by itself:** the step applies its own calls and logs an `auto` row. Unsure things in it are still asked, every time. An `auto` row stays `auto` (counts as clean) unless Matt says it got something wrong.
- **Going on the Ask line:** if Matt says a step got something wrong, at any time and in any session: fix it, change that issue's row to `wrong` with what was wrong, add the step to the `Ask:` line with the date and why, and tell him in one line it'll ask him again. If the mistake suggests a rule, offer the rule change too.
- **While on the Ask line:** the run still applies its own pick (so the issue is complete), then shows it to Matt in the end message. No reply means he agrees.
- **Coming off it:** check steps (tips, items, social, fixes, topup) after 6 issues in a row marked `clean`. Taste steps (puzzle, preheader, LinkedIn) once Matt took the pick unedited in at least 5 of the last 6 issues. `replay`, `unknown` and `skipped` rows don't count and don't break a streak. When one qualifies, take it off and tell him in one line in the end message: "I'll stop asking about <step>. Say if I get one wrong."

Ask: none.

Laptop runs (not phone mode) still stop at every step, as the skills say, and log rows the same way.

## How to log

One row per step per issue, added by the skill at its approval step, once Matt has answered and the change is applied. A step that didn't run (skipped, nothing to review) gets a row with `skipped` and why, so a streak isn't broken or faked.

| Step | Proposed | Result is `clean` when |
| --- | --- | --- |
| `tips` | counts: keep / drop / unsure | Matt flipped nothing, edited nothing, and every unsure went the way you leaned |
| `items` | counts: keep / changed / drop / unsure | no flips, no field edits, no moves or fixes asked for after |
| `social` | how many shown, which you'd add | he added exactly the ones you'd add |
| `puzzle` | the 3 answers, recommended first | `top pick` if he took #1 unedited |
| `preheader` | the 3 angles, which you recommended | `top pick` if he took it unedited |
| `linkedin` | the one draft | `top pick` if he approved it unedited |
| `fixes` | how many problems check-newsletter found | he ran every fix you suggested, as suggested, and asked for nothing else |

Otherwise write `changed` (check steps) or `other pick` / `edited` / `new round` (taste steps), and list each change in a few words: "flipped 2 drop to keep (old but relevant)", "retagged 1: no umbracocms", "picked #3".

## Log

| Issue | Step | Proposed | Matt's changes | Result |
| --- | --- | --- | --- | --- |
| 2026-11-25 | tips | replay: 1 keep / 3 drop | none | replay: agrees |
| 2026-11-25 | items | not recorded | moved 2 breaking changes to top of HQ | changed |
| 2026-11-25 | preheader | 3 angles, recommendation not recorded | picked #2, unedited | unknown |
| 2026-11-18 | tips | replay: 2 keep / 0 drop | none | replay: agrees |
| 2026-11-18 | preheader | 3 angles, recommendation not recorded | picked #3, unedited | unknown |
| 2026-11-11 | tips | replay: 3 keep / 0 drop | none | replay: agrees |
| 2026-11-11 | preheader | 3 angles, then 3 more | picked #4 from second round | new round |
| 2026-11-04 | tips | replay: 2 keep / 1 drop | none (the SafeMedia blog post was a duplicate of the package, sent 28-10-2026; rule 2) | replay: agrees |
| 2026-10-28 | tips | replay: 2 keep / 2 drop | none | replay: agrees |
| 2026-10-28 | items | not recorded | retagged 1: no umbracocms on a community post | changed |
| 2026-10-21 | tips | replay: 2 keep / 1 drop | none | replay: agrees |

Rows for issues before 2026-12-02 were rebuilt from `picks.md`, `tag-corrections.md` and `asks.md`. Other steps weren't recorded before then.

`replay` rows (25-11-2026): each past tip judged again under today's rules, against what went out. They check keep or drop only, not the link, title or tags, and are judged with hindsight, so they show the trend but don't count towards a streak. Older weeks weren't replayed: the rules were learned from them, so they'd only agree with themselves.
