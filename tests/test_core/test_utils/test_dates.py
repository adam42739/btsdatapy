from src.btsdatapy.core.utils.dates import iterate_year_months


def test_iterate_year_months():
    start = (2023, 3)
    end = (2024, 6)

    expected = [
        {"cboYear": "2023", "cboPeriod": "3"},
        {"cboYear": "2023", "cboPeriod": "4"},
        {"cboYear": "2023", "cboPeriod": "5"},
        {"cboYear": "2023", "cboPeriod": "6"},
        {"cboYear": "2023", "cboPeriod": "7"},
        {"cboYear": "2023", "cboPeriod": "8"},
        {"cboYear": "2023", "cboPeriod": "9"},
        {"cboYear": "2023", "cboPeriod": "10"},
        {"cboYear": "2023", "cboPeriod": "11"},
        {"cboYear": "2023", "cboPeriod": "12"},
        {"cboYear": "2024", "cboPeriod": "1"},
        {"cboYear": "2024", "cboPeriod": "2"},
        {"cboYear": "2024", "cboPeriod": "3"},
        {"cboYear": "2024", "cboPeriod": "4"},
        {"cboYear": "2024", "cboPeriod": "5"},
        {"cboYear": "2024", "cboPeriod": "6"},
    ]
    result = list(iterate_year_months(start, end))

    assert result == expected
