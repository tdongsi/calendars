"""
Test classes and functions for regular calendar.
Use unittest module as the main test framework.
"""

from datetime import date
import unittest

from calendars.calendars import RegularDate


class IsCurrentYearTest(unittest.TestCase):
    """
    Test cases for is_current_year and is_previous_year properties of calendars.RegularDate.
    """

    def test_general(self):

        today = RegularDate(date.today())
        # today should be in current calendar year
        self.assertEqual(today.is_current_year, True)
        self.assertEqual(today.is_previous_year, False)

    def test_year2018(self):
        """Pretend today as different dates in year 2018.
        """
        todays = [date(2018, 6, 15),
                  date(2018, 1, 1),
                  date(2018, 12, 31)
                  ]

        for today in todays:
            self._year2018_test_cases(today)
        pass

    def _year2018_test_cases(self, today):
        """ Test instances in year 2018, depending on what today is.
        """

        input_date = RegularDate(date(2018, 1, 1), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = RegularDate(date(2018, 12, 31), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = RegularDate(date(2018, 6, 15), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = RegularDate(date(2017, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = RegularDate(date(2017, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = RegularDate(date(2017, 6, 15), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = RegularDate(date(2019, 1, 1), today)
        self._verify_current_calendar_year(input_date)
        input_date = RegularDate(date(2019, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, False)
        input_date = RegularDate(date(2016, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, False)
        input_date = RegularDate(date(2016, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, False)

    def _verify_current_calendar_year(self, input_date, expected_current=False, expected_previous=False):
        """
        Verify the values of is_current_year and is_previous_year properties with expected output.
        """
        self.assertEqual(input_date.is_current_year, expected_current)
        self.assertEqual(input_date.is_previous_year, expected_previous)


class RegularDateTest(unittest.TestCase):
    """
    Test cases for other properties of calendars.RegularDate that are simple enough.
    """

    def test_string_output(self):
        my_date = RegularDate(date(2015, 12, 31))
        self.assertEqual(my_date.year_dates_string, "2015 (01-Jan-2015 - 31-Dec-2015)")
        self.assertEqual(my_date.year_string, "2015")

    pass