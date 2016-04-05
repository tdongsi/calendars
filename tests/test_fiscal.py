"""
Test classes and functions for fiscal calendar.
Use unittest module as the main test framework.
"""

from datetime import date, timedelta
import unittest

from calendars.calendars import FiscalDate

# TODO (tdongsi): Verify regular calendar = fiscal calendar with start date (1,1)


class FiscalDateTest(unittest.TestCase):
    """
    Test cases for other properties that are simple enough.
    """

    def test_date_to_fy(self):

        expected = (date(2014, 8, 1), date(2015, 7, 31))
        self.assertEqual(FiscalDate(date(2015, 6, 30)).year, 2015)
        self.assertEqual(FiscalDate.get_fiscal_start_end(date(2015, 6, 30)), expected)

        expected = (date(2015,8,1), date(2016,7,31))
        self.assertEqual(FiscalDate(date(2015, 8, 30)).year, 2016)
        self.assertEqual(FiscalDate.get_fiscal_start_end(date(2015, 8, 30)), expected)

        expected = (date(2015,8,1), date(2016,7,31))
        self.assertEqual(FiscalDate(date(2015, 8, 1)).year, 2016)
        self.assertEqual(FiscalDate.get_fiscal_start_end(date(2015, 8, 1)), expected)

        expected = (date(2014,8,1), date(2015,7,31))
        self.assertEqual(FiscalDate(date(2015, 7, 31)).year, 2015)
        self.assertEqual(FiscalDate.get_fiscal_start_end(date(2015, 7, 31)), expected)
        pass