import unittest
from stats_submission import StatsSubmission

class TestStatsSubmission(unittest.TestCase):
    def test_object_creation(self):
        sub = StatsSubmission(42, "2025-01-01", 3, 2)
        self.assertEqual(sub.playerId, 42)
        self.assertEqual(sub.goals, 3)
        self.assertEqual(sub.assists, 2)
        self.assertEqual(sub.date, "2025-01-01")

if __name__ == "__main__":
    unittest.main()
