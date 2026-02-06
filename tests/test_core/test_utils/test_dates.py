from src.btsdatapy.core.utils.dates import iterate_year_months


def test_iterate_year_months():
    start = (2023, 3)
    end = (2024, 6)

    expected = [
        {"cboYear": "2023", "cboMonth": "3"},
        {"cboYear": "2023", "cboMonth": "4"},
        {"cboYear": "2023", "cboMonth": "5"},
        {"cboYear": "2023", "cboMonth": "6"},
        {"cboYear": "2023", "cboMonth": "7"},
        {"cboYear": "2023", "cboMonth": "8"},
        {"cboYear": "2023", "cboMonth": "9"},
        {"cboYear": "2023", "cboMonth": "10"},
        {"cboYear": "2023", "cboMonth": "11"},
        {"cboYear": "2023", "cboMonth": "12"},
        {"cboYear": "2024", "cboMonth": "1"},
        {"cboYear": "2024", "cboMonth": "2"},
        {"cboYear": "2024", "cboMonth": "3"},
        {"cboYear": "2024", "cboMonth": "4"},
        {"cboYear": "2024", "cboMonth": "5"},
        {"cboYear": "2024", "cboMonth": "6"},
    ]
    result = list(iterate_year_months(start, end))

    assert result == expected
