from datetime import date

from calendars.calendars import FiscalDate


def main():

    first_fd = FiscalDate(date(2016, 8, 15))
    print first_fd.year
    print first_fd.quarter_start_date

    # Another company may have another fiscal date.
    # Change fiscal date to September 1st.
    FiscalDate.FISCAL_START_MONTH = 9
    second_fd = FiscalDate(date(2016, 8, 15))
    print second_fd.year
    print first_fd.year

    print second_fd.quarter_end_date

    pass


if __name__ == "__main__":
    main()
