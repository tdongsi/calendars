"""
Test classes and functions for lunar calendar.
Use unittest module as the main test framework.
"""

from datetime import date
import unittest

from calendars.calendars import LunarDate


class IsCurrentYearTest(unittest.TestCase):
    """
    Test cases for is_current_year and is_previous_year properties of calendars.LunarDate.
    """

    def test_general(self):

        today = LunarDate(date.today())
        # today should be in current calendar year
        self.assertEqual(today.is_current_year, True)
        self.assertEqual(today.is_previous_year, False)

    def test_year2018(self):
        """Pretend today as different dates in year 2018.
        """
        todays = [date(2018, 6, 15),
                  date(2018, 2, 16),
                  date(2019, 2, 4)
                  ]

        for today in todays:
            self._year2018_test_cases(today)
        pass

    def _year2018_test_cases(self, today):
        """ Test instances in year 2018, depending on what today is.
        """

        input_date = LunarDate(date(2018, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, True)
        input_date = LunarDate(date(2018, 2, 15), today)
        self._verify_current_calendar_year(input_date, False, True)
        input_date = LunarDate(date(2018, 2, 16), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = LunarDate(date(2018, 12, 31), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = LunarDate(date(2018, 6, 15), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = LunarDate(date(2017, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, False)

        input_date = LunarDate(date(2017, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = LunarDate(date(2017, 6, 15), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = LunarDate(date(2019, 1, 1), today)
        self._verify_current_calendar_year(input_date, True, False)
        input_date = LunarDate(date(2019, 1, 3), today)
        self._verify_current_calendar_year(input_date, True, False)
        input_date = LunarDate(date(2019, 2, 4), today)
        self._verify_current_calendar_year(input_date, True, False)
        input_date = LunarDate(date(2019, 2, 5), today)
        self._verify_current_calendar_year(input_date, False, False)

        input_date = LunarDate(date(2019, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, False)
        input_date = LunarDate(date(2016, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, False)
        input_date = LunarDate(date(2016, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, False)

    def _verify_current_calendar_year(self, input_date, expected_current=False, expected_previous=False):
        """
        Verify the values of is_current_year and is_previous_year properties with expected output.
        """
        self.assertEqual(input_date.is_current_year, expected_current)
        self.assertEqual(input_date.is_previous_year, expected_previous)


class LunarDateTest(unittest.TestCase):
    """
    Test cases for other properties of calendars.LunarDate that are simple enough.
    """

    def test_quarter(self):
        # Test case based on this:
        # https://s-media-cache-ak0.pinimg.com/736x/9b/5b/69/9b5b69fb9df56510a4b0a9ea488be305.jpg
        my_date = LunarDate(date(2016, 4, 8))
        self.assertEqual(my_date.quarter, 1)
        self.assertEqual(my_date.quarter_start_date, date(2016, 2, 8))
        self.assertEqual(my_date.quarter_end_date, date(2016, 5, 6))

        my_date = LunarDate(date(2016, 2, 1))
        self.assertEqual(my_date.quarter, 4)
        self.assertEqual(my_date.quarter_start_date, date(2015, 11, 12))
        self.assertEqual(my_date.quarter_end_date, date(2016, 2, 7))

    def test_string_output(self):
        my_date = LunarDate(date(2015, 12, 31))
        self.assertEqual(my_date.year_dates_string, "2015 (19-Feb-2015 - 07-Feb-2016)")
        self.assertEqual(my_date.year_string, "2015 - 2016")

    pass