import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import dedupe


def row(ts, host="h1", check="cpu"):
    return {"timestamp": ts, "host": host, "check": check, "message": "m"}


class TestDedupe(unittest.TestCase):
    def test_within_window_dropped(self):
        kept, dropped = dedupe([row("2026-10-31T09:00:00"), row("2026-10-31T09:30:00")], 60)
        self.assertEqual((len(kept), dropped), (1, 1))

    def test_after_window_kept(self):
        kept, dropped = dedupe([row("2026-10-31T09:00:00"), row("2026-10-31T10:30:00")], 60)
        self.assertEqual((len(kept), dropped), (2, 0))

    def test_different_check_kept(self):
        kept, dropped = dedupe([row("2026-10-31T09:00:00"), row("2026-10-31T09:10:00", check="disk")], 60)
        self.assertEqual((len(kept), dropped), (2, 0))
