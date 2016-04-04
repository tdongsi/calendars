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

# Each fiscal year starts on August 1st.
FISCAL_START = (8, 1)


class RegularDate(object):
    pass


class FiscalDate(object):
    pass


class RetailDate(object):
    pass
