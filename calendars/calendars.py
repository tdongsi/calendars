"""
Created on April 2nd, 2016

Utility classes for the following calendars:

1) Regular solar calendar
2) Fiscal calendar, based on class constant FISCAL_START.
3) Retail calendar, based on class constant FISCAL_START.
4) ISO calendar.

More information about retail calendar (a.k.a. 4-4-5 calendar):
https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar

@author: tdongsi
"""

from datetime import date, timedelta


class CalendarImplError(Exception):
    """ Raise this error when a property in the base class, e.g. BaseDate, is not overridden or implemented.
    """
    pass


class BaseDate(object):
    """
    The base calendar class for polymorphism and shared property implementations
    """

    def __init__(self, mdate):
        """ Initialize a date in regular calendar with the given datetime.date object.

        :param mdate: the given datetime.date object.
        :return:
        """
        self.__date = mdate

    @property
    def year(self):
        return self.__date.year

    @property
    def year_start_date(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def year_end_date(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def is_current_year(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def is_previous_year(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def quarter(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def quarter_start_date(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def quarter_end_date(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def is_current_quarter(self):
        raise CalendarImplError("Not implemented")
        pass

    @property
    def is_previous_quarter(self):
        raise CalendarImplError("Not implemented")
        pass

    #################################
    # Shared implementation
    #################################

    @property
    def year_num_of_days(self):
        """ Number of days in the calendar year containing this date instance.
        """
        diff = self.year_end_date - self.year_start_date
        return diff.days + 1

    @property
    def quarter_num_of_days(self):
        """ Number of days in the calendar quarter containing this date instance.
        """
        diff = self.quarter_end_date - self.quarter_start_date
        return diff.days + 1

    #################################
    # String format properties
    #################################

    @property
    def year_string(self):
        """ Year string with both years.
        E.g.: 2015 - 2016 for fiscal year 2016.
        """
        return "%d - %d" % (self.year_start_date.year, self.year_end_date.year)

    @property
    def year_dates_string(self):
        """ Year string with formatted starting and ending dates.
        E.g.: 2016 (26-JUL-2015 - 30-JUL-2016)
        """
        start_string = self.year_start_date.strftime("%d-%b-%Y")
        end_string = self.year_end_date.strftime("%d-%b-%Y")
        return "%d (%s - %s)" % (self.year, start_string, end_string)

    @property
    def quarter_string(self):
        """ Quarter string.
        E.g.: Quarter 3
        """
        return "Quarter " + str(self.quarter)

    @property
    def quarter_dates_string(self):
        """ Quarter string with formatted starting and ending dates.
        E.g.: 2016 (26-JUL-2015 - 30-JUL-2016)
        """
        start_string = self.quarter_start_date.strftime("%d-%b-%Y")
        end_string = self.quarter_end_date.strftime("%d-%b-%Y")
        return "%d (%s - %s)" % (self.quarter, start_string, end_string)


class RegularDate(BaseDate):
    """
    This utility class converts a given datetime.date instance into a REGULAR calendar's date instance with
    different pre-computed attributes of interest such as quarter starting date, week starting date for that date, etc.
    """

    # quarter's starting and ending dates
    _QUARTER_NUM_TO_DATE = { 1: ((1, 1), (3, 31)),
                             2: ((4, 1), (6, 30)),
                             3: ((7, 1), (9, 30)),
                             4: ((10, 1), (12, 31))}

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
        """
        return self._date.year

    @property
    def year_start_date(self):
        """ Start date of the calendar year containing this date instance.
        """
        return self.year_start

    @property
    def year_end_date(self):
        """ End date of the calendar year containing this date instance.
        """
        return self.year_end

    @property
    def is_current_year(self):
        """ Is this instance in the current calendar year, if today is as given?
        """
        return True if (self._today.year == self.year) else False

    @property
    def is_previous_year(self):
        """ Is the given date in the previous calendar year, if today is as given?
        """
        return True if (self._today.year - 1 == self.year) else False

    @property
    def quarter(self):
        """ Find the quarter number for the given date.

        Quarter is based on month (every three months), which is one-based in self._date.
        :return: Quarter number for the input date.
        """
        zero_based_month = self._date.month - 1
        quarter_num = zero_based_month / 3 + 1
        return quarter_num

    @property
    def quarter_start_date(self):
        """ Find the starting date of the quarter that contains the given date.
        """
        start_date = self._QUARTER_NUM_TO_DATE[self.quarter][0]
        return date(self.year, *start_date)

    @property
    def quarter_end_date(self):
        """ Find the ending date of the quarter that contains the given date.
        """
        end_date = self._QUARTER_NUM_TO_DATE[self.quarter][1]
        return date(self.year, *end_date)

    #################################
    # String format properties
    #################################

    @property
    def year_string(self):
        """ String of the current year.

        For regular calendar, override base implementation to print one year.
        """
        return str(self.year)

    pass


class FiscalDate(BaseDate):
    """
    This utility class converts a given datetime.date instance into a FISCAL calendar's date instance with
    different pre-computed attributes of interest such as quarter starting date, week starting date for that date, etc.

    To use for another fiscal calendar (e.g., different fiscal month), it is user's responsibility to update all
    internal class constants properly before creating FiscalDate instances:

    _FISCAL_START_MONTH
    _FISCAL_START_DAY
    _QUARTER_NUM_TO_DATE
    """
    # Each fiscal year starts on August 1st.
    _FISCAL_START_MONTH = 8
    _FISCAL_START_DAY = 1

    # quarter's starting and ending dates
    # It is easier and less error-prone to edit this constant than write code
    _QUARTER_NUM_TO_DATE = { 1: ((8, 1), (10, 31)),
                             2: ((11, 1), (1, 31)),
                             3: ((2, 1), (4, 30)),
                             4: ((5, 1), (7, 31))}

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
        if mdate < date(mdate.year, FiscalDate._FISCAL_START_MONTH, FiscalDate._FISCAL_START_DAY):
            year_start = date(mdate.year - 1, FiscalDate._FISCAL_START_MONTH, FiscalDate._FISCAL_START_DAY)
            year_end = date(mdate.year, FiscalDate._FISCAL_START_MONTH, FiscalDate._FISCAL_START_DAY) - timedelta(1)
        else:
            year_start = date(mdate.year, FiscalDate._FISCAL_START_MONTH, FiscalDate._FISCAL_START_DAY)
            year_end = date(mdate.year + 1, FiscalDate._FISCAL_START_MONTH, FiscalDate._FISCAL_START_DAY) - timedelta(1)
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
        """
        return self.year_start

    @property
    def year_end_date(self):
        """ End date of the fiscal year containing this date instance.
        """
        return self.year_end

    @property
    def is_current_year(self):
        """ Is this instance in the current fiscal year, if today is as given?
        """
        _, today_year_end = self.get_fiscal_start_end(self._today)
        return True if (today_year_end.year == self.year) else False

    @property
    def is_previous_year(self):
        """ Is the given date in the previous fiscal year, if today is as given?
        """
        _, today_year_end = self.get_fiscal_start_end(self._today)
        return True if (today_year_end.year - 1 == self.year) else False

    @property
    def quarter(self):
        """ Find the fiscal quarter number for the given date.

        Quarter is based on month (every three months), which is one-based in self._date.
        :return: Quarter number for the input date.
        """
        if self._date.year == self.year - 1:
            zero_based_month = self._date.month - self._FISCAL_START_MONTH
            quarter_num = zero_based_month / 3 + 1
            return quarter_num
        else:
            zero_based_month = self._date.month + 12 - self._FISCAL_START_MONTH
            quarter_num = zero_based_month / 3 + 1
            return quarter_num

    @property
    def quarter_start_date(self):
        """ Find the starting date of the quarter that contains the given date.
        """
        # Make sure the starting date of the first quarter is as defined.
        assert self._QUARTER_NUM_TO_DATE[1][0] == (self._FISCAL_START_MONTH, self._FISCAL_START_DAY)

        start_date = self._QUARTER_NUM_TO_DATE[self.quarter][0]
        start_year = self.year if self.quarter > 2 else self.year-1
        return date(start_year, *start_date)

    @property
    def quarter_end_date(self):
        """ Find the ending date of the quarter that contains the given date.
        """
        # Make sure the starting date of the first quarter is as defined.
        assert self._QUARTER_NUM_TO_DATE[1][0] == (self._FISCAL_START_MONTH, self._FISCAL_START_DAY)

        end_date = self._QUARTER_NUM_TO_DATE[self.quarter][1]
        end_year = self.year if self.quarter > 1 else self.year-1
        return date(end_year, *end_date)

    #################################
    # String format properties
    #################################

    pass


class RetailDate(BaseDate):
    """
    This utility class converts a given datetime.date instance into a RETAIL calendar's date instance with
    different pre-computed attributes of interest such as quarter starting date, week starting date for that date, etc.

    More on Retail calendar: https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar
    """
    # Each fiscal year starts on August 1st.
    # Retail calendar's end date is the last Saturday of the month at fiscal year end.
    FISCAL_START_MONTH = 8
    FISCAL_START_DAY = 1
    # Weeks in each month: Grouping of 13 weeks in a quarter can be 5-4-4 or 4-4-5.
    WEEKS_IN_MONTH = (5, 4, 4)

    def __init__(self, mdate, today=None):
        """ Initialize a date in retail calendar with the given datetime.date object.

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

        self.year_start, self.year_end = RetailDate.get_retail_start_end(self._date)
        pass

    @staticmethod
    def get_retail_start_end(mdate):
        """ Get the retail year's starting and ending dates that contain the given date

        :param mdate: the given date.
        :return:
        """

        retail_end = RetailDate.retail_end_by_year(mdate.year)

        if mdate <= retail_end:
            # mdate is in the current retail year
            year_start = RetailDate.retail_end_by_year(mdate.year-1) + timedelta(1)
            year_end = retail_end
        else:
            # mdate is in the next retail year
            year_start = retail_end + timedelta(1)
            year_end = RetailDate.retail_end_by_year(mdate.year+1)

        return year_start, year_end

    @staticmethod
    def retail_end_by_year(year):
        """ Retail calendar's year end for the given year.
        Retail calendar's end date is the last Saturday of the month at fiscal year end.

        :param year:
        :return:
        """
        fiscal_start = date(year, RetailDate.FISCAL_START_MONTH, RetailDate.FISCAL_START_DAY)
        # if fiscal_start is Sunday, then it's a retail start.
        # Otherwise, it is the very last Sunday.
        if fiscal_start.weekday() == 6:
            retail_start = fiscal_start
        else:
            # If Monday, weekday() == 0, move it back by 1 day
            # If Saturday, weekday() = 5, move it back by 6 days
            retail_start = fiscal_start - timedelta(fiscal_start.weekday() + 1)

        # Retail year end is simply the day before that.
        return retail_start-timedelta(1)

    @property
    def year(self):
        """ Return the retail year of the given date.

        Retail year is defined as the year number of the retail year end.
        :return:
        """
        return self.year_end.year

    @property
    def year_start_date(self):
        """ Start date of the retail year containing this date instance.
        """
        return self.year_start

    @property
    def year_end_date(self):
        """ End date of the retail year containing this date instance.
        """
        return self.year_end

    @property
    def is_current_year(self):
        """ Is this instance in the current retail year, if today is as given?
        """
        _, today_year_end = self.get_retail_start_end(self._today)
        return True if (today_year_end.year == self.year) else False

    @property
    def is_previous_year(self):
        """ Is the given date in the previous retail year, if today is as given?
        """
        _, today_year_end = self.get_retail_start_end(self._today)
        return True if (today_year_end.year - 1 == self.year) else False

    #################################
    # String format properties
    #################################

    pass
