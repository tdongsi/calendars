"""
Test classes and functions for fiscal calendar.
Use unittest module as the main test framework.
"""

from datetime import date, timedelta
import unittest

from freezegun import freeze_time

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

        expected = (date(2015, 8, 1), date(2016, 7, 31))
        self.assertEqual(FiscalDate(date(2015, 8, 30)).year, 2016)
        self.assertEqual(FiscalDate.get_fiscal_start_end(date(2015, 8, 30)), expected)

        expected = (date(2015, 8, 1), date(2016, 7, 31))
        self.assertEqual(FiscalDate(date(2015, 8, 1)).year, 2016)
        self.assertEqual(FiscalDate.get_fiscal_start_end(date(2015, 8, 1)), expected)

        expected = (date(2014, 8, 1), date(2015, 7, 31))
        self.assertEqual(FiscalDate(date(2015, 7, 31)).year, 2015)
        self.assertEqual(FiscalDate.get_fiscal_start_end(date(2015, 7, 31)), expected)
        pass


class IsCurrentFiscalYearTest(unittest.TestCase):
    """
    Test cases for is_current_year properties.
    """

    def test_fiscal_year(self):

        today = FiscalDate(date.today())
        # today should be in current fiscal year
        self.assertEqual(today.is_current_year, True)

        input_date = date.today() + timedelta(days=400)
        self.assertEqual(FiscalDate(input_date).is_current_year, False)

        input_date = date.today() - timedelta(days=400)
        self.assertEqual(FiscalDate(input_date).is_current_year, False)

        # date way in the past should not be
        input_date = date(2012, 12, 21)
        self.assertEqual(FiscalDate(input_date).is_current_year, False)

        pass

    def test_fiscal_year_2009(self):
        """
        Mock today() as a day during fiscal year 2010 (2009-08-01 to 2010-07-31)
        """
        todays = [date(2009, 10, 1),   # random earlier half
                  date(2010, 2, 1),    # random later half
                  date(2009, 12, 31),   # start of calendar year
                  date(2010, 1, 1),   # end of calendar year
                  date(2009, 8, 1),   # start of fiscal year
                  date(2010, 7, 31),   # end of fiscal year
                  ]

        for today_2010 in todays:
            self._fiscal_2009_2010_test_cases(today_2010)
        pass

    def _fiscal_2009_2010_test_cases(self, today):
        # Mock output of today() with today, using freezegun
        with freeze_time(today):
            # At False boundary
            input_date = date(2009, 7, 24)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2009, 7, 25)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2010, 8, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2010, 8, 2)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)

            # At True boundary
            input_date = date(2009, 7, 26)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2009, 7, 27)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2010, 7, 29)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2010, 7, 30)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)

            # Next month lower end
            input_date = date(2009, 7, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2009, 8, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2009, 8, 2)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)

            # Next month higher end
            input_date = date(2010, 7, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2010, 8, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2010, 8, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)

            # Calendar year end
            input_date = date(2008, 12, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2009, 12, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2010, 12, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)

            # Calendar year start
            input_date = date(2009, 1, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2010, 1, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2011, 1, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)

    def test_fiscal_year_2006(self):
        """
        Mock today() as a day during fiscal year 2006 (2005-08-01 to 2006-07-31)
        """
        todays = [date(2005, 10, 1),   # random earlier half
                  date(2006, 2, 1),    # random later half
                  date(2005, 12, 31),   # start of calendar year
                  date(2006, 1, 1),   # end of calendar year
                  date(2005, 8, 1),   # start of fiscal year
                  date(2006, 7, 31),   # end of fiscal year
                  ]

        for today_2006 in todays:
            self._fiscal_2005_2006_test_cases(today_2006)

    def _fiscal_2005_2006_test_cases(self, today):
        # Mock output of today() with today, using freezegun
        with freeze_time(today):
            # At False boundary
            input_date = date(2005, 7, 30)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2006, 7, 30)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            # At True boundary
            input_date = date(2005, 7, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2006, 7, 29)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            # Next month lower end
            input_date = date(2005, 8, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2005, 8, 2)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            # Next month higher end
            input_date = date(2006, 7, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2006, 8, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2006, 8, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            # Calendar year end
            input_date = date(2004, 12, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2005, 12, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2006, 12, 31)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            # Calendar year start
            input_date = date(2005, 1, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)
            input_date = date(2006, 1, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, True)
            input_date = date(2007, 1, 1)
            self.assertEqual(FiscalDate(input_date).is_current_year, False)

        pass
