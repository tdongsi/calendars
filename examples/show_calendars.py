from datetime import date

import calendars.calendars as cc


def main():
    my_date = date(2016, 4, 8)
    cal = cc.RegularDate(my_date)
    fy = cc.FiscalDate(my_date)
    r544 = cc.RetailDate(my_date)
    # TODO: ISO and lunar calendar

    fiscal_attr = [fy.year,
                   fy.year_string,
                   fy.year_dates_string,
                   fy.year_start_date,
                   fy.year_end_date,
                   fy.year_num_of_days,
                   fy.is_current_year,
                   fy.is_previous_year,
                   fy.quarter,
                   fy.quarter_string,
                   fy.quarter_dates_string,
                   fy.quarter_start_date,
                   fy.quarter_end_date,
                   fy.quarter_num_of_days,
                   ]

    r544_attr = [r544.year,
                 r544.year_string,
                 r544.year_dates_string,
                 r544.year_start_date,
                 r544.year_end_date,
                 r544.year_num_of_days,
                 r544.is_current_year,
                 r544.is_previous_year,
                 r544.quarter,
                 r544.quarter_string,
                 r544.quarter_dates_string,
                 r544.quarter_start_date,
                 r544.quarter_end_date,
                 r544.quarter_num_of_days,
                 ]

    regular_attr = [cal.year,
                   cal.year_string,
                   cal.year_dates_string,
                   cal.year_start_date,
                   cal.year_end_date,
                   cal.year_num_of_days,
                   cal.is_current_year,
                   cal.is_previous_year,
                   cal.quarter,
                   cal.quarter_string,
                   cal.quarter_dates_string,
                   cal.quarter_start_date,
                   cal.quarter_end_date,
                   cal.quarter_num_of_days,
                    ]

    print fiscal_attr
    print r544_attr
    print regular_attr

if __name__ == "__main__":
    main()