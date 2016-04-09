from datetime import date, timedelta
import unittest

from calendars.calendars import IsoDate


class IsoYearStartEnd(unittest.TestCase):
    """Test IsoDate.year_start_date and IsoDate.year_end_date properties.
    """

    def test_start_date_output(self):
        """ Sanity tests: if the input date is start date of the Iso year,
        the year_start_date should be the same.
        """

        # Sanity test
        iso_date = IsoDate(date(2018, 1, 1))
        self.assertEqual(iso_date.year_start_date, date(2018, 1, 1))
        self.assertEqual(iso_date.year_end_date, date(2018, 12, 30))
        iso_date = IsoDate(date(2018, 12, 31))
        self.assertEqual(iso_date.year_start_date, date(2018, 12, 31))
        self.assertEqual(iso_date.year_end_date, date(2019, 12, 29))

        # All tests using datetime's isocalendar
        for year in xrange(1990, 2020):
            my_date = date(year, 6, 15)
            iso_date = IsoDate(my_date)

            year_start = iso_date.year_start_date.isocalendar()
            self.assertEqual(year_start[0], year)
            self.assertEqual(year_start[1], 1)
            self.assertEqual(year_start[2], 1)

            year_end = iso_date.year_end_date.isocalendar()
            self.assertEqual(year_end[0], year)
            self.assertTrue(year_end[1] >= 52, year)
            self.assertEqual(year_end[2], 7)

        pass


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
                  date(2018, 12, 30)
                  ]

        for today in todays:
            self._year2018_test_cases(today)
        pass

    def _year2018_test_cases(self, today):
        """ Test instances in year 2018, depending on what today is.
        """

        input_date = IsoDate(date(2018, 1, 1), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = IsoDate(date(2018, 12, 30), today)
        self._verify_current_calendar_year(input_date, True, False)
        input_date = IsoDate(date(2018, 12, 31), today)
        self._verify_current_calendar_year(input_date, False, False)

        input_date = IsoDate(date(2018, 6, 15), today)
        self._verify_current_calendar_year(input_date, True, False)

        input_date = IsoDate(date(2017, 1, 1), today)
        self._verify_current_calendar_year(input_date, False, False)
        input_date = IsoDate(date(2017, 1, 2), today)
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
        self.assertEqual(my_date.quarter_start_date, date(2016, 4, 4))
        self.assertEqual(my_date.quarter_end_date, date(2016, 7, 3))

    def test_quarter_start_end(self):
        for year in xrange(1990, 2020):
            my_date = IsoDate(date(year, 2, 15))
            self.assertEqual(my_date.quarter, 1)
            self.assertEqual(my_date.quarter_start_date.isocalendar(), (year, 1, 1))
            self.assertEqual(my_date.quarter_end_date.isocalendar(), (year, 13, 7))

            my_date = IsoDate(date(year, 5, 15))
            self.assertEqual(my_date.quarter, 2)
            self.assertEqual(my_date.quarter_start_date.isocalendar(), (year, 14, 1))
            self.assertEqual(my_date.quarter_end_date.isocalendar(), (year, 26, 7))
        pass

    def test_string_output(self):
        my_date = IsoDate(date(2015, 12, 31))
        self.assertEqual(my_date.year_dates_string, "2015 (29-Dec-2014 - 03-Jan-2016)")
        self.assertEqual(my_date.year_string, "2015")

    pass