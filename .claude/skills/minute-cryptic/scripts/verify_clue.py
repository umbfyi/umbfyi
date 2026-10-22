#!/usr/bin/env python3
"""Mechanically verify cryptic clues.

Usage:
  python verify_clue.py clues.json        # file with one clue object or a list
  echo '{...}' | python verify_clue.py -  # stdin

Each clue object:
  clue        full clue text including enumeration, e.g. "... (7)"
  answer      the solution, e.g. "UMBRACO" (spaces/hyphens allowed for multi-word)
  definition  the definition words, must sit at the start or end of the clue
  device      anagram | hidden | reversal | hidden_reversal | charade | container
              | initials | deletion | double_definition
  indicator   indicator word(s) (not needed for a plain charade or a double
              definition)

Device-specific fields:
  anagram          fodder: [clue words whose letters are rearranged]
  hidden           fodder: the clue span the answer hides in
  reversal         fodder: clue word(s) that read backwards give the answer
  hidden_reversal  fodder: clue span containing the answer backwards
  charade          parts: [{"text": clue words, "yields": letters}, ...] in order
  container        outer: {"text","yields"}, inner: {"text","yields"}
  initials         fodder: clue span whose first letters spell the answer
  deletion         fodder: {"text","yields"} the word letters are dropped from
                   drop: first | last | ends | middle, or {"text","yields"} for
                   specific letters named in the clue
  double_definition  definition2: the second definition, at the other end of
                   the clue; only a short link word (and, or, is, for...) may
                   sit between the two. Both meanings are always flagged for a
                   human check, since code can't verify them.

Two devices: one charade part, or the container's outer or inner, may add
  "device": anagram | reversal | hidden | initials | deletion, plus its own
  "indicator" (and "drop": first | last | ends | middle for a deletion).
  Its yields are then checked from its literal text. Max one such part.

Exit code 0 if every clue passes, 1 otherwise. Warnings don't fail a clue,
but they flag things a human should look at.
"""
import json
import re
import sys


def letters(s):
    return re.sub(r"[^A-Za-z]", "", s).upper()


def in_clue(fragment, clue):
    return fragment.strip().lower() in clue.lower()


def enumeration_of(answer):
    words = re.split(r"[\s]+", answer.strip())
    parts = []
    for w in words:
        hy = w.split("-")
        parts.append("-".join(str(len(letters(h))) for h in hy))
    return ",".join(parts)


POSITIONS = ("first", "last", "ends", "middle")

# Words allowed between the two halves of a double definition.
LINK_WORDS = {"and", "or", "is", "for", "as", "gives", "makes", "becomes", "of", "with", "in", "to", "from", "but"}


def drop_by_position(fl, drop):
    mid = len(fl) // 2
    return {
        "first": fl[1:],
        "last": fl[:-1],
        "ends": fl[1:-1],
        "middle": fl[:mid] + fl[mid + 1:] if len(fl) % 2 else fl[:mid - 1] + fl[mid + 1:],
    }[drop]


def check_part(p, surface, errors, warnings):
    """Check one charade/container part and return the letters it yields.

    A part may carry its own device (the clue's second device), which is
    verified from its literal text instead of being trusted.
    """
    text, yields = p.get("text", ""), letters(p.get("yields", ""))
    if not in_clue(text, surface):
        errors.append(f"part '{text}' not found in clue")
    sub = p.get("device", "").lower()
    if not sub:
        if letters(text) != yields:
            warnings.append(
                f"'{text}' -> '{p.get('yields')}' relies on an abbreviation "
                "or synonym; check it's standard"
            )
        return yields

    ind = p.get("indicator", "")
    if not ind:
        errors.append(f"{sub} part '{text}' needs an indicator")
    elif not in_clue(ind, surface):
        errors.append(f"indicator '{ind}' not found in clue")

    t = letters(text)
    if sub == "anagram":
        got_ok = sorted(t) == sorted(yields) and t != yields
    elif sub == "reversal":
        got_ok = t[::-1] == yields
    elif sub == "hidden":
        got_ok = yields in t and yields != t
    elif sub == "initials":
        got_ok = "".join(letters(w)[:1] for w in text.split()) == yields
    elif sub == "deletion":
        drop = p.get("drop", "")
        if drop not in POSITIONS:
            errors.append(f"deletion part '{text}' needs drop: first | last | ends | middle")
            return yields
        got_ok = drop_by_position(t, drop) == yields
    else:
        errors.append(f"unknown part device '{sub}'")
        return yields
    if not got_ok:
        errors.append(f"{sub} of '{text}' doesn't give {yields}")
    return yields


def check(c):
    errors, warnings = [], []
    clue = c.get("clue", "")
    answer = c.get("answer", "")
    ans = letters(answer)
    device = c.get("device", "").lower()

    if not clue or not ans:
        return ["clue and answer are required"], warnings

    # Enumeration
    m = re.search(r"\(([\d,\-\s]+)\)\s*$", clue)
    if not m:
        errors.append("clue must end with an enumeration like (7) or (3,4)")
        surface = clue
    else:
        given = re.sub(r"\s", "", m.group(1))
        expected = enumeration_of(answer)
        if given != expected:
            errors.append(f"enumeration ({given}) doesn't match answer ({expected})")
        surface = clue[: m.start()].strip()

    # Definition at start or end
    d = c.get("definition", "")
    s_norm = re.sub(r"[^\w\s]", "", surface).strip().lower()
    d_norm = re.sub(r"[^\w\s]", "", d).strip().lower()
    if not d_norm:
        errors.append("definition is required")
    elif not (s_norm.startswith(d_norm) or s_norm.endswith(d_norm)):
        errors.append(f"definition '{d}' must be at the start or end of the clue")
    elif ans in letters(d):
        errors.append("definition contains the answer")

    # Indicator
    ind = c.get("indicator", "")
    if device not in ("charade", "double_definition"):
        if not ind:
            errors.append(f"{device} needs an indicator")
        elif not in_clue(ind, surface):
            errors.append(f"indicator '{ind}' not found in clue")

    # A deletion's fodder usually contains the answer (ANODE minus A = NODE),
    # so only look for the answer outside the fodder.
    visible = surface
    if device == "deletion" and isinstance(c.get("fodder"), dict):
        visible = re.sub(re.escape(c["fodder"].get("text", "")), " ", surface, flags=re.I)
    if ans in letters(visible) and device not in ("hidden",):
        errors.append("answer appears in plain sight in the clue")

    if device == "anagram":
        fodder = c.get("fodder", [])
        if isinstance(fodder, str):
            fodder = [fodder]
        for f in fodder:
            if not in_clue(f, surface):
                errors.append(f"fodder '{f}' not found in clue")
        fl = letters("".join(fodder))
        if sorted(fl) != sorted(ans):
            extra = sorted((set(fl) - set(ans)))
            errors.append(
                f"anagram letters don't match: fodder={''.join(sorted(fl))} "
                f"answer={''.join(sorted(ans))}"
            )
        elif fl == ans:
            errors.append("fodder is already the answer, not an anagram")

    elif device in ("hidden", "hidden_reversal"):
        span = c.get("fodder", "")
        if not in_clue(span, surface):
            errors.append(f"span '{span}' not found in clue")
        target = ans if device == "hidden" else ans[::-1]
        if target not in letters(span):
            errors.append(f"'{target}' is not hidden in '{span}'")
        else:
            for word in span.split():
                if target in letters(word):
                    warnings.append("answer sits inside a single word; spanning words is fairer")

    elif device == "reversal":
        f = c.get("fodder", "")
        f = " ".join(f) if isinstance(f, list) else f
        if not in_clue(f, surface):
            errors.append(f"fodder '{f}' not found in clue")
        if letters(f)[::-1] != ans:
            errors.append(f"'{letters(f)}' reversed is '{letters(f)[::-1]}', not {ans}")

    elif device == "charade":
        parts = c.get("parts", [])
        if len(parts) < 2:
            errors.append("charade needs at least two parts")
        if sum(1 for p in parts if p.get("device")) > 1:
            errors.append("max 2 devices: only one part may have its own device")
        joined = "".join(check_part(p, surface, errors, warnings) for p in parts)
        if joined != ans:
            errors.append(f"parts join to {joined}, not {ans}")

    elif device == "container":
        o, i = c.get("outer", {}), c.get("inner", {})
        if o.get("device") and i.get("device"):
            errors.append("max 2 devices: only one of outer/inner may have its own device")
        ol =check_part(o, surface, errors, warnings)
        il = check_part(i, surface, errors, warnings)
        if not any(ol[:k] + il + ol[k:] == ans for k in range(1, len(ol))):
            errors.append(f"{il} inside {ol} can't make {ans}")

    elif device == "initials":
        span = c.get("fodder", "")
        if not in_clue(span, surface):
            errors.append(f"span '{span}' not found in clue")
        firsts = "".join(letters(w)[:1] for w in span.split())
        if firsts != ans:
            errors.append(f"first letters of '{span}' spell {firsts}, not {ans}")

    elif device == "deletion":
        f = c.get("fodder", {})
        if not in_clue(f.get("text", ""), surface):
            errors.append(f"fodder '{f.get('text')}' not found in clue")
        if letters(f.get("text", "")) != letters(f.get("yields", "")):
            warnings.append(
                f"'{f.get('text')}' -> '{f.get('yields')}' relies on an abbreviation "
                "or synonym; check it's standard"
            )
        fl = letters(f.get("yields", ""))
        drop = c.get("drop", "")
        if isinstance(drop, dict):
            if not in_clue(drop.get("text", ""), surface):
                errors.append(f"dropped part '{drop.get('text')}' not found in clue")
            if letters(drop.get("text", "")) != letters(drop.get("yields", "")):
                warnings.append(
                    f"'{drop.get('text')}' -> '{drop.get('yields')}' relies on an abbreviation "
                    "or synonym; check it's standard"
                )
            dl = letters(drop.get("yields", ""))
            results = {fl[:k] + fl[k + len(dl):] for k in range(len(fl)) if dl and fl[k:k + len(dl)] == dl}
            if ans not in results:
                errors.append(f"removing {dl} from {fl} can't make {ans}")
        elif drop in POSITIONS:
            result = drop_by_position(fl, drop)
            if result != ans:
                errors.append(f"{fl} with {drop} letter(s) dropped is {result}, not {ans}")
        else:
            errors.append("deletion needs drop: first | last | ends | middle | {text, yields}")

    elif device == "double_definition":
        d2 = c.get("definition2", "")
        d2_norm = re.sub(r"[^\w\s]", "", d2).strip().lower()
        if not d2_norm:
            errors.append("double_definition needs definition2")
        elif d_norm:
            if s_norm.startswith(d_norm) and s_norm.endswith(d2_norm):
                middle = s_norm[len(d_norm):len(s_norm) - len(d2_norm)]
            elif s_norm.startswith(d2_norm) and s_norm.endswith(d_norm):
                middle = s_norm[len(d2_norm):len(s_norm) - len(d_norm)]
            else:
                middle = None
                errors.append("the two definitions must sit at opposite ends of the clue")
            if middle is not None:
                extra = [w for w in middle.split() if w not in LINK_WORDS]
                if extra or len(middle.split()) > 1:
                    errors.append(f"only one short link word may sit between the definitions, found '{middle.strip()}'")
            if ans in letters(d2):
                errors.append("definition2 contains the answer")
        warnings.append(f"check both meanings by hand: '{d}' and '{d2}' must each define {ans}")

    else:
        errors.append(f"unknown device '{device}'")

    return errors, warnings


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    data = json.load(sys.stdin if src == "-" else open(src))
    clues = data if isinstance(data, list) else [data]
    all_ok = True
    for n, c in enumerate(clues, 1):
        errors, warnings = check(c)
        status = "PASS" if not errors else "FAIL"
        all_ok &= not errors
        print(f"[{status}] #{n} {c.get('clue', '')}  ->  {c.get('answer', '')}")
        for e in errors:
            print(f"    error: {e}")
        for w in warnings:
            print(f"    warn:  {w}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
