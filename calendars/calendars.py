"""
Created on April 2nd, 2016

Utility classes for the following calendars:

1) Regular solar calendar
2) Fiscal calendar, based on global FISCAL_START.
3) Retail calendar, based on global FISCAL_START.

More information about retail calendar (a.k.a. 4-4-5 calendar):
https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar

@author: tdongsi
"""

from datetime import date

# Each fiscal year starts on August 1st.
FISCAL_START = (8, 1)


class RegularDate(object):

    def __init__(self, mdate, today=None):
        """ Initialize a date in regular calendar with the given datetime.date object.

        :param mdate: the given datetime.date object.
        :param today: default is the current date (today), if not provided.
        :return:
        """
        self._date = mdate
        if not today:
            self._today = date.today()
        else:
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
    pass


class RetailDate(object):
    pass
