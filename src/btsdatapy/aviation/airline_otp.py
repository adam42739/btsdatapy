import pandas as pd
from btsdatapy.core.config import TABLE_CONFIGS
from btsdatapy.core.fetch import fetch_table
from btsdatapy.core.utils import iterate_year_months

_REPORTING_CARRIER_OTP_DEFAULT_COLUMNS = [
    "FlightDate",
    "ReportingAirline",
    "TailNumber",
    "ReportingAirlineFlightNumber",
    "OriginAirport",
    "DestinationAirport",
    "ScheduledDepartureTime",
    "ActualDepartureTime",
    "ScheduledArrivalTime",
    "ActualArrivalTime",
    "Cancelled",
]


def reporting_carrier_otp(
    start: tuple[int, int],
    end: tuple[int, int] | None = None,
    add: list[str] | None = None,
    remove: list[str] | None = None,
    only: list[str] | None = None,
) -> pd.DataFrame:
    """
    Retrieve Reporting Carrier On-Time Performance data.

    This function returns a pandas DataFrame containing historical U.S. domestic
    flight on-time performance data from the Bureau of Transportation Statistics (BTS).
    The resulting DataFrame includes a configurable set of columns based on the
    ``add``, ``remove``, and ``only`` parameters.

    By default, a predefined set of commonly used columns is returned. Callers may
    extend or reduce this set using ``add`` and ``remove``. Alternatively, ``only``
    may be used to explicitly specify the full set of columns to return.

    Some columns in the raw BTS data are code-based identifiers (e.g., airline codes,
    airport codes). These columns can be mapped to their descriptive names by prefixing the column name with
    an asterisk ``*`` (e.g. ``"*Airport"``).

    Parameters
    ----------
    start : tuple[int, int]
        A tuple specifying the starting year and month (inclusive) for the data
        retrieval in the format ``(year, month)``.

    end : tuple[int, int], optional
        A tuple specifying the ending year and month (inclusive) for the data
        retrieval in the format ``(year, month)``. If omitted, data for only the
        ``start`` month is retrieved.

    add : list of str, optional
        Additional columns to include in the result, appended to the default column
        set. Column names prefixed with ``"*"`` will be returned in their original
        code-based form rather than being mapped to descriptive values.

        Cannot be used together with ``only``.

    remove : list of str, optional
        Columns to remove from the default column set.

        Cannot be used together with ``only``.

    only : list of str, optional
        Explicit list of columns to return. When provided, the default column set is
        ignored and only the specified columns are included in the result.

        Cannot be used together with ``add`` or ``remove``.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing Reporting Carrier On-Time Performance data with the
        requested columns applied.

    Notes
    -----
    A complete list of available columns, as well as the set of default columns
    returned by this function, is documented in the project documentation.

    Examples
    --------
    Fetch data for April, 2023. Add an additional descriptive column to the default output:

    >>> df = reporting_carrier_otp((2023, 4), add=["*OriginAirport"])

    Fetch data from April, 2023 to October, 2025. Retain code-based identifiers instead of descriptive mappings:

    >>> df = reporting_carrier_otp(start=(2023, 4), end=(2025, 10), add=["Airline", "Airport"], remove=["*Airline", "*Airport"]) # "*Airline" and "*Airport" are default columns

    Fetch data for April, 2023. Specify an explicit set of columns:

    >>> df = reporting_carrier_otp((2023, 4), only=["FlightDate", "Carrier", "ArrivalDelay"])
    """  # noqa: E501
    table_config = TABLE_CONFIGS["aviation"]["airline_otp"]["reporting_carrier_otp"]
    columns = _REPORTING_CARRIER_OTP_DEFAULT_COLUMNS + ["*ReportingAirline"]
    all_user_parameters = iterate_year_months(start, end or start)

    df = fetch_table(table_config, columns, all_user_parameters)

    return df
