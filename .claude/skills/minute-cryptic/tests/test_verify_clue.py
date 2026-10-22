#!/usr/bin/env python3
"""Tests for scripts/verify_clue.py.

Run from anywhere:
  python3 tests/test_verify_clue.py
"""
import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "verify_clue.py"
spec = importlib.util.spec_from_file_location("verify_clue", SCRIPT)
verify_clue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify_clue)
check = verify_clue.check


def part(text, yields, **extra):
    return {"text": text, "yields": yields, **extra}


# Clues that must pass, grouped by device.
PASSING = [
    # anagram
    {"clue": "Confused cobra, um, becomes friendly CMS (7)", "answer": "UMBRACO",
     "definition": "friendly CMS", "device": "anagram", "indicator": "Confused",
     "fodder": ["cobra", "um"]},
    {"clue": "Reworked bug, Ed? Fix code (5)", "answer": "DEBUG", "definition": "Fix code",
     "device": "anagram", "indicator": "Reworked", "fodder": ["bug", "Ed"]},
    # hidden
    {"clue": "Fix inside code bugs (5)", "answer": "DEBUG", "definition": "Fix",
     "device": "hidden", "indicator": "inside", "fodder": "code bugs"},
    {"clue": "Fix code: some made bugs (5)", "answer": "DEBUG", "definition": "Fix code",
     "device": "hidden", "indicator": "some", "fodder": "made bugs"},
    # hidden reversal
    {"clue": "Fix code after ragu bedtime, going back (5)", "answer": "DEBUG",
     "definition": "Fix code", "device": "hidden_reversal", "indicator": "going back",
     "fodder": "ragu bedtime"},
    # reversal
    {"clue": "Stressed, returned for afters (8)", "answer": "DESSERTS",
     "definition": "afters", "device": "reversal", "indicator": "returned",
     "fodder": "Stressed"},
    # charade
    {"clue": "Dutch 'the' with bug makes fix (5)", "answer": "DEBUG", "definition": "fix",
     "device": "charade", "parts": [part("Dutch 'the'", "DE"), part("bug", "BUG")]},
    # initials
    {"clue": "Initially developers enjoy breaking useless gadgets? Fix (5)", "answer": "DEBUG",
     "definition": "Fix", "device": "initials", "indicator": "Initially",
     "fodder": "developers enjoy breaking useless gadgets"},
    # deletion by position
    {"clue": "Headless anode is part of a tree (4)", "answer": "NODE",
     "definition": "part of a tree", "device": "deletion", "indicator": "Headless",
     "fodder": part("anode", "ANODE"), "drop": "first"},
    {"clue": "Unwrapped scopes manage (4)", "answer": "COPE", "definition": "manage",
     "device": "deletion", "indicator": "Unwrapped", "fodder": part("scopes", "SCOPES"),
     "drop": "ends"},
    # deletion of named letters
    {"clue": "Fast store's cachet, no time (5)", "answer": "CACHE", "definition": "Fast store",
     "device": "deletion", "indicator": "no", "fodder": part("cachet", "CACHET"),
     "drop": part("time", "T")},
    # two devices: charade with a reversed part
    {"clue": "No Ed, returning, finds part of a tree (4)", "answer": "NODE",
     "definition": "part of a tree", "device": "charade",
     "parts": [part("No", "NO"), part("Ed", "DE", device="reversal", indicator="returning")]},
    # two devices: container with an anagram inside
    {"clue": "Church holding wild hac is fast store (5)", "answer": "CACHE",
     "definition": "fast store", "device": "container", "indicator": "holding",
     "outer": part("Church", "CE"),
     "inner": part("hac", "ACH", device="anagram", indicator="wild")},
    # double definition
    {"clue": "Hoard fast memory (5)", "answer": "CACHE", "definition": "Hoard",
     "device": "double_definition", "definition2": "fast memory"},
    {"clue": "Limb for parallel work (6)", "answer": "BRANCH", "definition": "parallel work",
     "device": "double_definition", "definition2": "Limb"},
]

# Clues that must fail, each with a phrase the error should contain.
FAILING = [
    ({"clue": "Initially developers enjoy fixing useless gadgets? Fix (5)", "answer": "DEBUG",
      "definition": "Fix", "device": "initials", "indicator": "Initially",
      "fodder": "developers enjoy fixing useless gadgets"},
     "spell DEFUG"),
    ({"clue": "Endless anode is part of a tree (4)", "answer": "NODE",
      "definition": "part of a tree", "device": "deletion", "indicator": "Endless",
      "fodder": part("anode", "ANODE"), "drop": "last"},
     "is ANOD, not NODE"),
    ({"clue": "Heartless robot gives fish (3)", "answer": "ROT", "definition": "fish",
      "device": "deletion", "indicator": "Heartless", "fodder": part("robot", "ROBOT"),
      "drop": "middle"},
     "is ROOT, not ROT"),
    ({"clue": "Node is part of a tree, anode headless (4)", "answer": "NODE",
      "definition": "part of a tree", "device": "deletion", "indicator": "headless",
      "fodder": part("anode", "ANODE"), "drop": "first"},
     "plain sight"),
    ({"clue": "No Ed, returning, finds part of a tree (4)", "answer": "NODE",
      "definition": "part of a tree", "device": "charade",
      "parts": [part("No", "NO", device="reversal", indicator="returning"),
                part("Ed", "DE", device="reversal", indicator="returning")]},
     "max 2 devices"),
    ({"clue": "No Ed, returning, finds part of a tree (4)", "answer": "NODE",
      "definition": "part of a tree", "device": "charade",
      "parts": [part("No", "NO"), part("Ed", "DE", device="anagram", indicator="shuffled")]},
     "indicator 'shuffled' not found"),
    ({"clue": "Confused cobra, um, becomes friendly CMS (6)", "answer": "UMBRACO",
      "definition": "friendly CMS", "device": "anagram", "indicator": "Confused",
      "fodder": ["cobra", "um"]},
     "enumeration (6)"),
    ({"clue": "Confused cobra, um, becomes friendly CMS (7)", "answer": "UMBRACO",
      "definition": "becomes", "device": "anagram", "indicator": "Confused",
      "fodder": ["cobra", "um"]},
     "must be at the start or end"),
    ({"clue": "Confused cobra, ma, becomes friendly CMS (7)", "answer": "UMBRACO",
      "definition": "friendly CMS", "device": "anagram", "indicator": "Confused",
      "fodder": ["cobra", "ma"]},
     "anagram letters don't match"),
    ({"clue": "Hoard of really fast memory (5)", "answer": "CACHE", "definition": "Hoard",
      "device": "double_definition", "definition2": "fast memory"},
     "only one short link word"),
    ({"clue": "Hoard fast memory (5)", "answer": "CACHE", "definition": "Hoard",
      "device": "double_definition"},
     "needs definition2"),
]


class PassingClues(unittest.TestCase):
    def test_passing(self):
        for c in PASSING:
            with self.subTest(clue=c["clue"]):
                errors, _ = check(c)
                self.assertEqual(errors, [])


class FailingClues(unittest.TestCase):
    def test_failing(self):
        for c, expected in FAILING:
            with self.subTest(clue=c["clue"], expected=expected):
                errors, _ = check(c)
                self.assertTrue(any(expected in e for e in errors), errors)


class Warnings(unittest.TestCase):
    def test_synonym_part_warns(self):
        _, warnings = check(PASSING[6])  # Dutch 'the' -> DE
        self.assertTrue(any("abbreviation or synonym" in w for w in warnings))

    def test_double_definition_always_warns(self):
        _, warnings = check(PASSING[-1])
        self.assertTrue(any("check both meanings" in w for w in warnings))

    def test_device_part_does_not_warn(self):
        _, warnings = check(PASSING[11])  # Ed reversed -> DE is checked, not trusted
        self.assertEqual(warnings, [])


class Enumeration(unittest.TestCase):
    def test_enumeration(self):
        for answer, expected in [
            ("DEBUG", "5"),
            ("I REMEMBER BEING DIRTY", "1,8,5,5"),
            ("WORKS ON MY MACHINE", "5,2,2,7"),
            ("HIGH-FIVE", "4-4"),
        ]:
            with self.subTest(answer=answer):
                self.assertEqual(verify_clue.enumeration_of(answer), expected)


class DropByPosition(unittest.TestCase):
    def test_positions(self):
        for word, drop, expected in [
            ("ANODE", "first", "NODE"),
            ("ANODE", "last", "ANOD"),
            ("SCOPES", "ends", "COPE"),
            ("ROBOT", "middle", "ROOT"),
            ("BOOK", "middle", "BK"),
        ]:
            with self.subTest(word=word, drop=drop):
                self.assertEqual(verify_clue.drop_by_position(word, drop), expected)


if __name__ == "__main__":
    unittest.main()
