"""
Test classes and functions for retail calendar.
Use unittest module as the main test framework.
"""

from datetime import date, timedelta
import unittest

from calendars.calendars import RetailDate


class RetailYearStartDate(unittest.TestCase):
    """Test RetailDate.year_start_date and RetailDate.year_end_date properties.

    The test cases assume fiscal date is August 1st.
    FISCAL_START_MONTH = 8
    FISCAL_START_DAY = 1
    """

    # dates: list of tuples of (month,day)
    dates = [(1, 1),
             (8, 1),
             (8, 2),
             (12, 31)]
    dates.extend([(7, day) for day in xrange(22, 32)])
    dates.sort()
    years = range(2000, 2020)

    # Start 544 year dates from 2000-2020
    start544_dates = [
        (1999, 8, 1),
        (2000, 7, 30),
        (2001, 7, 29),
        (2002, 7, 28),
        (2003, 7, 27),
        (2004, 8, 1),
        (2005, 7, 31),
        (2006, 7, 30),
        (2007, 7, 29),
        (2008, 7, 27),
        (2009, 7, 26),
        (2010, 8, 1),
        (2011, 7, 31),
        (2012, 7, 29),
        (2013, 7, 28),
        (2014, 7, 27),
        (2015, 7, 26),
        (2016, 7, 31),
        (2017, 7, 30),
        (2018, 7, 29),
        (2019, 7, 28)
    ]

    def test_output(self):
        """ Sanity tests: if the input date is start date of the retail year,
        the year_start_date should be the same.
        """

        self.assertEqual(RetailDate.FISCAL_START_MONTH, 8)
        self.assertEqual(RetailDate.FISCAL_START_DAY, 1)

        # map of input date -> expected output for start date of retail calendar
        input_to_output = {}

        # Construct the dict:
        # {
        #   start_date-1: previous_start_date,
        #   start_date : start_date,
        #   start_date+1: start_date
        # }
        for idx in xrange(len(self.years)):
            start_date = date(*self.start544_dates[idx])

            if idx != 0:
                input_to_output[start_date - timedelta(1)] = date(*self.start544_dates[idx-1])

            input_to_output[start_date] = start_date
            input_to_output[start_date + timedelta(1)] = date(*self.start544_dates[idx])

        # Verify the actual output and expected output from dict
        for k, v in input_to_output.iteritems():
            actual = RetailDate(k).year_start_date
            message = "Input: %s, Output: %s, Expected: %s" % (k, actual, v)
            self.assertEqual(actual, v, message)

        pass

    def test_aggr_date_input(self):
        """ Find all retail year's start dates for random input in 2000-2020 period.
        """

        actual_output_date = set([])
        for year in self.years:
            for my_date in self.dates:
                input_date = date(year, my_date[0], my_date[1])
                start544_date = RetailDate(input_date).year_start_date
                actual_output_date.add(start544_date)

        # Verify the start 544 dates
        expected_start_544 = set([date(mTup[0], mTup[1], mTup[2]) for mTup in self.start544_dates])
        diff = expected_start_544.symmetric_difference(actual_output_date)
        self.assertEqual(len(diff), 0, "Diff: " + str(diff))