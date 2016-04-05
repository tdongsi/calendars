# calendars

Utility classes for the following calendars with tests:

1. Regular solar calendar
2. Fiscal calendar, based on global FISCAL_START.
3. [Retail calendar](https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar), based on global FISCAL_START.

## Additional information

There are surprisingly many types of calendar. Some of them are:

1. **Regular Calendar**: regular solar calendar date range as we know. 
   * Example: January 01, 2006 to December 31, 2006.
1. [**Lunar Calendar**](https://en.wikipedia.org/wiki/Lunar_calendar): based on cycles of the lunar phases.
   * Example: January 29, 2006 to February 17, 2007.
   * A lunar year is defined as 12 lunations, which is about 354 days.
   * In every two or three years, a [thirteenth-month](https://en.wikipedia.org/wiki/Lunisolar_calendar) (intercalary month or leap month) is added to bring the calendar year into synchronisation with the solar year.
2. **Fiscal Calendar**: a company’s selected calendar date range for required SEC financial statement filing.
   * Example: August 01, 2005 to July 31, 2006 is my company's fiscal year 2006.
3. **Tax Calendar**: A number sequence representing weeks in a Tax year which begins right after the US Tax Day.
   * Example: April 16, 2005 to April 15, 2006.
4. **Retail Calendar**: also known as [4-4-5 Calendar](https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar) or 544 calendar. 544 describes the number of weeks for a given quarter. Each quarter begins with a 5 week "month", followed by 2 four week "months".
   * Example: July 31, 2005 to July 29, 2006.
   * Why? This calendar ensures all 4 quarters in a calendar year are equal. This allows comparing weekly data (e.g., retail sales) to the prior year without correcting for times when regular calendar weeks break across months or quarters.
   * How? It usually uses the same end month as the fiscal calendar and each retail week consists of Sunday through Saturday.
      * The retail year end is defined as "the last Saturday of the month at the fiscal year end".
      * If August 1st is Sunday, it is retail calendar's starting date. The Saturday July 31st is the last Saturday and end of the last retail year.
      * If August 1st is Monday, then Saturday July 30th is end of the last retail year, and July 31st is the start of the current retail year.
5. **ISO calendar**: provided in Python `datetime` module.
   * Example: January 02, 2006 to December 31, 2006.
   * The first week of an ISO year is the first (Gregorian/regular) calendar week of a year containing a Thursday.
   * Each week starts at Monday and ends at Sunday. 


Out of the above calendar types, retail calendar seems to have more complex rules. However, this calendar type is frequently used in industries like retail and manufacturing for ease of planning around it. 