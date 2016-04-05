"""
Test classes and functions for retail calendar.
Use unittest module as the main test framework.
"""

from datetime import date, timedelta
import unittest

from calendars.calendars import RetailDate


class RetailYearStartEnd(unittest.TestCase):
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

    # Retail year's start dates from 2000-2020
    retail_start_dates = [
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

    # Retail year's end dates from 2000-2020
    retail_end_dates = [
        (2000, 7, 29),
        (2001, 7, 28),
        (2002, 7, 27),
        (2003, 7, 26),
        (2004, 7, 31),
        (2005, 7, 30),
        (2006, 7, 29),
        (2007, 7, 28),
        (2008, 7, 26),
        (2009, 7, 25),
        (2010, 7, 31),
        (2011, 7, 30),
        (2012, 7, 28),
        (2013, 7, 27),
        (2014, 7, 26),
        (2015, 7, 25),
        (2016, 7, 30),
        (2017, 7, 29),
        (2018, 7, 28),
        (2019, 7, 27),
        (2020, 7, 25),
    ]

    def test_start_date_output(self):
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
            start_date = date(*self.retail_start_dates[idx])

            if idx != 0:
                input_to_output[start_date - timedelta(1)] = date(*self.retail_start_dates[idx - 1])

            input_to_output[start_date] = start_date
            input_to_output[start_date + timedelta(1)] = date(*self.retail_start_dates[idx])

        # Verify the actual output and expected output from dict
        for k, v in input_to_output.iteritems():
            actual = RetailDate(k).year_start_date
            message = "Input: %s, Output: %s, Expected: %s" % (k, actual, v)
            self.assertEqual(actual, v, message)

        pass

    def test_end_date_output(self):

        # map of input date -> expected output for end date of retail calendar
        input_to_output = {}

        # Construct the dict:
        # {
        #   end_date-1: end_date,
        #   end_date : end_date,
        #   end_date+1: next_end_date
        # }
        for idx in xrange(len(self.years)):
            start_date = date(*self.retail_end_dates[idx])

            input_to_output[start_date - timedelta(1)] = date(*self.retail_end_dates[idx])
            input_to_output[start_date] = start_date
            if idx != len(self.years)-1:
                input_to_output[start_date + timedelta(1)] = date(*self.retail_end_dates[idx + 1])

        for k, v in input_to_output.iteritems():
            actual = RetailDate(k).year_end_date
            message = "Input: %s, Output: %s, Expected: %s" % (k, actual, v)
            self.assertEqual(actual, v, message)

        pass

    def test_aggr_date_input(self):
        """ Find all retail year's start dates for random input in 2000-2020 period.
        """

        actual_start_date = set([])
        actual_end_date = set([])
        for year in self.years:
            for my_date in self.dates:
                input_date = date(year, my_date[0], my_date[1])
                retail_date = RetailDate(input_date)
                actual_start_date.add(retail_date.year_start_date)
                actual_end_date.add(retail_date.year_end_date)

        # Verify the retail start dates
        expected_start = set([date(mTup[0], mTup[1], mTup[2]) for mTup in self.retail_start_dates])
        diff = expected_start.symmetric_difference(actual_start_date)
        self.assertEqual(len(diff), 0, "Diff: " + str(diff))

        # Verify the retail end dates
        expected_end = set([date(mTup[0], mTup[1], mTup[2]) for mTup in self.retail_end_dates])
        diff = expected_end.symmetric_difference(actual_end_date)
        self.assertEqual(len(diff), 0, "Diff: " + str(diff))
