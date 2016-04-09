from datetime import date
import unittest

from calendars.calendars import IsoDate


class IsCurrentYearTest(unittest.TestCase):
    """
    Test cases for is_current_year and is_previous_year properties of calendars.IsoDate.
    """

    def test_general(self):

        today = IsoDate(date.today())
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

        input_date = IsoDate(date(2018, 1, 1), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = IsoDate(date(2018, 12, 31), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = IsoDate(date(2018, 6, 15), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = IsoDate(date(2017, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = IsoDate(date(2017, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = IsoDate(date(2017, 6, 15), today)
        self._verify_current_calendar_year(input_date, False, True)

        input_date = IsoDate(date(2019, 1, 1), today)
        self._verify_current_calendar_year(input_date)
        input_date = IsoDate(date(2019, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, False)
        input_date = IsoDate(date(2016, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, False)
        input_date = IsoDate(date(2016, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, False)

    def _verify_current_calendar_year(self, input_date, expected_current=False, expected_previous=False):
        """
        Verify the values of is_current_year and is_previous_year properties with expected output.
        """
        self.assertEqual(input_date.is_current_year, expected_current)
        self.assertEqual(input_date.is_previous_year, expected_previous)


class IsoDateTest(unittest.TestCase):
    """
    Test cases for other properties of calendars.IsoDate that are simple enough.
    """

    def test_quarter(self):
        my_date = IsoDate(date(2016, 4, 8))
        self.assertEqual(my_date.quarter, 2)
        self.assertEqual(my_date.quarter_start_date, date(2016, 4, 1))
        self.assertEqual(my_date.quarter_end_date, date(2016, 6, 30))

    def test_string_output(self):
        my_date = IsoDate(date(2015, 12, 31))
        self.assertEqual(my_date.year_dates_string, "2015 (01-Jan-2015 - 31-Dec-2015)")
        self.assertEqual(my_date.year_string, "2015")

    pass