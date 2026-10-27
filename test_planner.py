
import unittest
from planner import generate_plan


class TestPlanner(unittest.TestCase):

    def test_study_hours(self):
        plan = generate_plan(
            ["Python"],
            {"Python": "Hard"},
            2,
            1
        )

        self.assertEqual(plan[0]["Minutes"], 120)

    def test_difficulty_priority(self):
        plan = generate_plan(
            ["Python", "DBMS"],
            {"Python": "Hard", "DBMS": "Easy"},
            3,
            1
        )

        self.assertGreater(
            plan[0]["Minutes"],
            plan[1]["Minutes"]
        )

    def test_daily_time_limit(self):
        plan = generate_plan(
            ["Python", "DBMS", "Math"],
            {
                "Python": "Hard",
                "DBMS": "Medium",
                "Math": "Easy"
            },
            3,
            2
        )

        for day in [1, 2]:
            total = sum(
                item["Minutes"]
                for item in plan
                if item["Day"] == day
            )

            self.assertEqual(total, 180)


if __name__ == "__main__":
    unittest.main()
