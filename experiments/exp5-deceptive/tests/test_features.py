import unittest
from app import (
    render_invoice, render_receipt, render_summary,
    render_calendar, render_schedule, export_csv_name,
)


# Feature tests = the oracle. Each feature's correctness depends on exactly ONE
# candidate function, so "tests fixed by fixing function X" = X's blast radius.

class TestMoneyFeatures(unittest.TestCase):   # depend only on money()
    def test_invoice(self):
        self.assertEqual(render_invoice(1005), "INVOICE total: $10.05")

    def test_receipt(self):
        self.assertEqual(render_receipt(2500), "RECEIPT: $25.00 paid")

    def test_summary(self):
        self.assertEqual(render_summary(900), "Summary - $9.00")


class TestDateFeatures(unittest.TestCase):     # depend only on _pad2()/format_date
    def test_calendar(self):
        self.assertEqual(render_calendar(2026, 3, 7), "Calendar: 2026-03-07")

    def test_schedule(self):
        self.assertEqual(render_schedule(2026, 1, 9), "Scheduled for 2026-01-09")


class TestSlugFeature(unittest.TestCase):      # depends only on slugify_title()
    def test_csv_name(self):
        self.assertEqual(export_csv_name("My Q1 Report!"), "my-q1-report.csv")


if __name__ == "__main__":
    unittest.main()
