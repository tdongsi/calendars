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
import pycalcal.pycalcal as pycal


def cumsum(alist):
    """ A generator that return a cumulative running sum of elements in a list.

    :param alist: list of numeric.
    :yield: the current running sum.
    """
    tot = 0
    for e in alist:
        tot += e
        yield tot


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
    different pre-computed attributes of interest such as quarter starting date for that date, etc.
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
    different pre-computed attributes of interest such as quarter starting date for that date, etc.

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
    different pre-computed attributes of interest such as quarter starting date for that date, etc.

    More on Retail calendar: https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar
    """
    # Each fiscal year starts on August 1st.
    # Retail calendar's end date is the last Saturday of the month at fiscal year end.
    FISCAL_START_MONTH = 8
    FISCAL_START_DAY = 1
    # Weeks in each month: Grouping of 13 weeks in a quarter can be 5-4-4 or 4-4-5.
    WEEKS_IN_MONTH = [5, 4, 4]*4

    # In the case of 53-week, the extra week is put in the last month. In this case, last quarter is (5, 4, 5)
    LEAP_MONTH = 12

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

        self.is_53_week = True if self.year_num_of_days == 53 * 7 else False
        # Create an instance copy
        self._weeks_in_month = self.WEEKS_IN_MONTH[:]
        if self.is_53_week:
            # Add additional week to the leap month
            self._weeks_in_month[self.LEAP_MONTH-1] += 1

        self.weeks_in_quarter = [sum(self._weeks_in_month[0:3]),
                            sum(self._weeks_in_month[3:6]),
                            sum(self._weeks_in_month[6:9]),
                            sum(self._weeks_in_month[9:12])]
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

    @property
    def quarter(self):
        """ Find the retail quarter number for the given date.

        Quarter is based on month (every three months), which is one-based in self._date.
        :return: Quarter number for the input date.
        """
        num_days = (self._date - self.year_start_date).days
        week_num = num_days / 7

        week_cumsum = [0]
        week_cumsum.extend(cumsum(self.weeks_in_quarter))
        count = 0
        for count in xrange(1, len(week_cumsum)):
            if week_cumsum[count-1] <= week_num < week_cumsum[count]:
                break
        return count

    @property
    def quarter_start_date(self):
        """ Find the starting date of the quarter that contains the given date.
        """
        # Find the running total of weeks per quarter
        week_cumsum = [0]
        week_cumsum.extend(cumsum(self.weeks_in_quarter))
        start_date = self.year_start_date + timedelta(week_cumsum[self.quarter-1]*7)
        return start_date

    @property
    def quarter_end_date(self):
        """ Find the ending date of the quarter that contains the given date.
        """
        # Find the running total of weeks per quarter
        week_cumsum = list(cumsum(self.weeks_in_quarter))
        end_date = self.year_start_date + timedelta(week_cumsum[self.quarter-1]*7-1)
        return end_date

    #################################
    # String format properties
    #################################

    pass


class IsoDate(BaseDate):
    """
    This utility class converts a given datetime.date instance into a ISO calendar's date instance with
    different pre-computed attributes of interest such as quarter starting date for that date, etc.

    http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm
    https://en.wikipedia.org/wiki/ISO_week_date
    """

    # Weeks in each month: Grouping of 13 weeks in a quarter can be 5-4-4 or 4-4-5.
    WEEKS_IN_MONTH = [5, 4, 4]*4
    # In the case of 53-week, the extra week is put in the last month. In this case, last quarter is (5, 4, 5)
    LEAP_MONTH = 12

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

        self._year = self._date.isocalendar()[0]
        self.year_start = self.iso_year_start(self._date)
        self.year_end = self.iso_year_end(self._date)

        self.is_53_week = True if self.year_num_of_days == 53 * 7 else False
        # Create an instance copy
        self._weeks_in_month = self.WEEKS_IN_MONTH[:]
        if self.is_53_week:
            # Add additional week to the leap month
            self._weeks_in_month[self.LEAP_MONTH-1] += 1

        self.weeks_in_quarter = [sum(self._weeks_in_month[0:3]),
                            sum(self._weeks_in_month[3:6]),
                            sum(self._weeks_in_month[6:9]),
                            sum(self._weeks_in_month[9:12])]

    def iso_year_start(self, mdate):
        """ Find starting date of ISO year that contains the given date.

        The first week of the ISO calendar year is the earliest week that contains at least 4 days of January.
        It follows that 4th January is the latest that week 1 can start.
        :param mdate: the input date
        :return: starting date of ISO year.
        """
        forth_jan = date(mdate.isocalendar()[0], 1, 4)
        year_start = forth_jan + timedelta(days=1-forth_jan.isocalendar()[2])
        return year_start

    def iso_year_end(self, mdate):
        """ Find ending date of ISO year that contains the given date.

        4th January is the latest that week 1 can start.
        :param mdate:
        :return:
        """
        forth_jan = date(mdate.isocalendar()[0]+1, 1, 4)
        year_end = forth_jan - timedelta(days=forth_jan.isocalendar()[2])
        return year_end

    @property
    def year(self):
        """ Return the calendar year of the given date.
        """
        return self._year

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
        return True if (self._today.isocalendar()[0] == self.year) else False

    @property
    def is_previous_year(self):
        """ Is the given date in the previous calendar year, if today is as given?
        """
        return True if (self._today.isocalendar()[0] - 1 == self.year) else False

    @property
    def quarter(self):
        """ Find the retail quarter number for the given date.

        Quarter is based on month (every three months), which is one-based in self._date.
        :return: Quarter number for the input date.
        """
        num_days = (self._date - self.year_start_date).days
        week_num = num_days / 7

        week_cumsum = [0]
        week_cumsum.extend(cumsum(self.weeks_in_quarter))
        count = 0
        for count in xrange(1, len(week_cumsum)):
            if week_cumsum[count-1] <= week_num < week_cumsum[count]:
                break
        return count

    @property
    def quarter_start_date(self):
        """ Find the starting date of the quarter that contains the given date.
        """
        # Find the running total of weeks per quarter
        week_cumsum = [0]
        week_cumsum.extend(cumsum(self.weeks_in_quarter))
        start_date = self.year_start_date + timedelta(week_cumsum[self.quarter-1]*7)
        return start_date

    @property
    def quarter_end_date(self):
        """ Find the ending date of the quarter that contains the given date.
        """
        # Find the running total of weeks per quarter
        week_cumsum = list(cumsum(self.weeks_in_quarter))
        end_date = self.year_start_date + timedelta(week_cumsum[self.quarter-1]*7-1)
        return end_date

    #################################
    # String format properties
    #################################

    @property
    def year_string(self):
        """ String of the current year.

        For ISO calendar, just like regular calendar, override base implementation to print one year.
        """
        return str(self.year)

    pass


class LunarDate(BaseDate):
    """
    This utility class converts a given datetime.date instance into a LUNAR calendar's date instance with
    different pre-computed attributes of interest such as quarter starting date for that date, etc.
    """

    def __init__(self, mdate, today=None):
        """ Initialize a date in lunar calendar with the given datetime.date object.

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

        self._chinese_date = self.lunar_from_regular(self._date)
        fixed_date = pycal.fixed_from_gregorian((self._date.year, self._date.month, self._date.day))
        self._chinese_date = pycal.chinese_from_fixed(fixed_date)
        cycle, year, month, leap_month, day = self._chinese_date
        self._year = self.normalize_lunar_year(cycle, year)
        self._month = month
        self._day = day

        # chinese_new_year_on_or_before does not work
        self._year_start = self.regular_from_lunar((cycle, year, 1, leap_month, 1))
        self._year_end = self.regular_from_lunar((cycle, year + 1, 1, leap_month, 1)) - timedelta(1)

    def normalize_lunar_year(self, cycle, year):
        """ Normalize lunar year to make it close to solar year number.

        The Chinese year 0 starts from 2697 BC (Yellow King legend).
        We don't want that extra 2697 to keep lunar year number close to solar year number.
        :param cycle:
        :param year:
        :return:
        """
        return cycle * 60 + year - 2697

    def lunar_from_regular(self, rdate):
        """Get lunar date from regular date.

        :param rdate: Python datetime module's date class.
        :return: cdate: a tuple of format (cycle, offset, month, leap, day) defined by PyCalCal.
        """
        fixed_date = pycal.fixed_from_gregorian((rdate.year, rdate.month, rdate.day))
        chinese_date = pycal.chinese_from_fixed(fixed_date)
        return chinese_date

    def regular_from_lunar(self, cdate):
        """ Get regular date from lunar date.

        :param cdate: a tuple of format (cycle, offset, month, leap, day) defined by PyCalCal.
        :return: corresponding date in regular Gregorian calendar.
        """
        rdate = pycal.gregorian_from_fixed(pycal.fixed_from_chinese(cdate))
        return date(*rdate)

    @property
    def year(self):
        """ Return the calendar year of the given date.
        """
        return self._year

    @property
    def year_start_date(self):
        """ Start date of the calendar year containing this date instance.
        """
        return self._year_start

    @property
    def year_end_date(self):
        """ End date of the calendar year containing this date instance.
        """
        return self._year_end

    @property
    def is_current_year(self):
        """ Is this instance in the current calendar year, if today is as given?
        """
        cycle, year, _, _, _ = self.lunar_from_regular(self._today)
        today_year = self.normalize_lunar_year(cycle, year)
        return True if (today_year == self.year) else False

    @property
    def is_previous_year(self):
        """ Is the given date in the previous calendar year, if today is as given?
        """
        cycle, year, _, _, _ = self.lunar_from_regular(self._today)
        today_year = self.normalize_lunar_year(cycle, year)
        return True if (today_year - 1 == self.year) else False

    @property
    def quarter(self):
        """ Find the quarter number for the given date.

        Quarter is based on month (every three months), which is one-based in self._date.
        :return: Quarter number for the input date.
        """
        zero_based_month = self._month - 1
        quarter_num = zero_based_month / 3 + 1
        return quarter_num

    @property
    def quarter_start_date(self):
        """ Find the starting date of the quarter that contains the given date.
        """
        cycle, year, _, leap_month, _ = self._chinese_date
        month = self.quarter * 3 - 2
        # Find first day of month 1, 4, 7, 10 for quarters.
        quarter_start = self.regular_from_lunar((cycle, year, month, leap_month, 1))
        return quarter_start

    @property
    def quarter_end_date(self):
        """ Find the ending date of the quarter that contains the given date.
        """
        if self.quarter == 4:
            return self.year_end_date

        cycle, year, _, leap_month, _ = self._chinese_date
        month = self.quarter * 3 + 1
        # Find first day of the next quarter: month 4, 7, 10 for quarters.
        quarter_end = self.regular_from_lunar((cycle, year, month, leap_month, 1))
        return quarter_end - timedelta(1)

    #################################
    # String format properties
    #################################

    pass