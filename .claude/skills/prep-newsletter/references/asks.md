# Prep asks log

Things Matt asked for during newsletter prep that the skills didn't do by themselves, and how they went. Read at the start of each prep; anything that keeps coming up should move into a skill. Format and rules: `../SKILL.md`, "Log Matt's asks". Newest issue first. This repo is public: no private data.

## 2026-11-25

- **Ask:** Move the two breaking change announcements to the top of Umbraco HQ. They were added at positions 3 and 5, sorted by date.
  - **Did:** Matt moved them by hand in the backoffice (skills couldn't reorder yet).
  - **Outcome:** Fixed before send.
  - **Suggestion:** Server sort puts ⚠️ / 🚨 / "breaking change" / "security advisory" items first in their group; `newsletter-items` step 9 and `check-newsletter` check it. Done: newsletter-items, check-newsletter (server sort waits on a deploy).
- **Ask:** Fixes after the page is built (edits, reorders) had to be handed to Matt.
  - **Did:** Nothing then.
  - **Outcome:** Matt did them by hand.
  - **Suggestion:** `umbfyi.sh edit-item` and `move-block`, used by `newsletter-items` step 9 and `prep-newsletter` step 8. Done: newsletter-items, prep-newsletter.
