def iterate_year_months(
    start: tuple[int, int],
    end: tuple[int, int],
    year_key: str = "cboYear",
    month_key: str = "cboPeriod",
) -> list[dict[str, str]]:
    start_year, start_month = start
    end_year, end_month = end

    year_months = []
    for year in range(start_year, end_year + 1):
        month_start = start_month if year == start_year else 1
        month_end = end_month if year == end_year else 12
        for month in range(month_start, month_end + 1):
            year_months.append({year_key: str(year), month_key: str(month)})

    return year_months
