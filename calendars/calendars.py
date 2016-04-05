"""
Created on April 2nd, 2016

Utility classes for the following calendars:

1) Regular solar calendar
2) Fiscal calendar, based on class constant FISCAL_START.
3) Retail calendar, based on class constant FISCAL_START.

More information about retail calendar (a.k.a. 4-4-5 calendar):
https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar

@author: tdongsi
"""

from datetime import date, timedelta


class RegularDate(object):
    """
    This utility class converts a given datetime.date instance into a REGULAR calendar's date instance with
    different pre-computed attributes of interest such as quarter starting date, week starting date for that date, etc.
    """

    def __init__(self, mdate, today=None):
        """ Initialize a date in regular calendar with the given datetime.date object.

        :param mdate: the given datetime.date object.
        :param today: default is the current date (today), if not specified.
        :return:
        """
        self._date = mdate
        if not today:
            self._today = date.today()
        else:
            # Useful when verifying functionality when running on a particular date.
            self._today = today

        self.year_start = date(self._date.year, 1, 1)
        self.year_end = date(self._date.year, 12, 31)

    @property
    def year(self):
        """ Return the calendar year of the given date.

        :return:
        """
        return self._date.year

    @property
    def year_start_date(self):
        """ Start date of the calendar year containing this date instance.

        :return:
        """
        return self.year_start

    @property
    def year_end_date(self):
        """ End date of the calendar year containing this date instance.

        :return:
        """
        return self.year_end

    @property
    def year_num_of_days(self):
        """ Number of days in the calendar year containing this date instance.

        :return: Number of days in the calendar year containing this date instance.
        """
        diff = self.year_end - self.year_start
        return diff.days + 1

    @property
    def is_current_year(self):
        """ Is this instance in the current calendar year, if today is as given?

        :return: True/False
        """
        return True if (self._today.year == self.year) else False

    @property
    def is_previous_year(self):
        """ Is the given date in the previous calendar year, if today is as given?

        :return:
        """
        return True if (self._today.year - 1 == self.year) else False

    pass


class FiscalDate(object):
    """
    This utility class converts a given datetime.date instance into a FISCAL calendar's date instance with
    different pre-computed attributes of interest such as quarter starting date, week starting date for that date, etc.
    """
    # Each fiscal year starts on August 1st.
    FISCAL_START_MONTH = 8
    FISCAL_START_DAY = 1

    def __init__(self, mdate, today=None):
        """ Initialize a date in fiscal calendar with the given datetime.date object.

        :param mdate: the given datetime.date object.
        :param today: default is the current date (today), if not specified.
        :return:
        """
        self._date = mdate
        if not today:
            self._today = date.today()
        else:
            # Useful when verifying functionality when running on a particular date.
            self._today = today

        self.year_start, self.year_end = FiscalDate.get_fiscal_start_end(self._date)
        pass

    @staticmethod
    def get_fiscal_start_end(mdate):
        """ Get the fiscal year's starting and ending dates that contain the given date

        :param mdate: the given date.
        :return:
        """
        if mdate.month < FiscalDate.FISCAL_START_MONTH:
            year_start = date(mdate.year - 1, FiscalDate.FISCAL_START_MONTH, FiscalDate.FISCAL_START_DAY)
            year_end = date(mdate.year, FiscalDate.FISCAL_START_MONTH, FiscalDate.FISCAL_START_DAY) - timedelta(1)
        else:
            year_start = date(mdate.year, FiscalDate.FISCAL_START_MONTH, FiscalDate.FISCAL_START_DAY)
            year_end = date(mdate.year + 1, FiscalDate.FISCAL_START_MONTH, FiscalDate.FISCAL_START_DAY) - timedelta(1)
        return year_start, year_end

    @property
    def year(self):
        """ Return the fiscal year of the given date.

        Fiscal year is defined as the year number of the fiscal year end.
        :return:
        """
        return self.year_end.year

    @property
    def year_start_date(self):
        """ Start date of the fiscal year containing this date instance.

        :return:
        """
        return self.year_start

    @property
    def year_end_date(self):
        """ End date of the fiscal year containing this date instance.

        :return:
        """
        return self.year_end

    @property
    def year_num_of_days(self):
        """ Number of days in the fiscal year containing this date instance.

        :return: Number of days in the fiscal year containing this date instance.
        """
        diff = self.year_end - self.year_start
        return diff.days + 1

    @property
    def is_current_year(self):
        """ Is this instance in the current fiscal year, if today is as given?

        :return: True/False
        """
        _, today_year_end = self.get_fiscal_start_end(self._today)
        return True if (today_year_end.year == self.year) else False

    @property
    def is_previous_year(self):
        """ Is the given date in the previous fiscal year, if today is as given?

        :return:
        """
        _, today_year_end = self.get_fiscal_start_end(self._today)
        return True if (today_year_end.year - 1 == self.year) else False

    pass


class RetailDate(object):
    pass
