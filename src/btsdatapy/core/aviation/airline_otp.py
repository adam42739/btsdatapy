from btsdatapy.core.models import BtsTableRequestPayload
from btsdatapy.core.utils.obfuscation import rot13

REPORTING_CARRIER_OTP_TABLE_ID: str = "FGJ"
REPORTING_CARRIER_OTP_SH146_NAME: str = rot13("o0-time")

MARKETING_CARRIER_OTP_TABLE_ID: str = "FGK"
MARKETING_CARRIER_OTP_SH146_NAME: str = rot13("o0-time")


class ReportingCarrierOTPPayload(BtsTableRequestPayload):
    txtSearch: str = ""

    cboGeography: str = "All"
    cboYear: str = "2025"
    cboPeriod: str = "1"
    btnDownload: str = "Download"

    YEAR: str | None = None

    QUARTER: str | None = None
    MONTH: str | None = None
    DAY_OF_MONTH: str | None = None
    DAY_OF_WEEK: str | None = None
    FL_DATE: str | None = None

    OP_UNIQUE_CARRIER: str | None = None
    OP_CARRIER_AIRLINE_ID: str | None = None
    OP_CARRIER: str | None = None
    TAIL_NUM: str | None = None
    OP_CARRIER_FL_NUM: str | None = None

    ORIGIN_AIRPORT_ID: str | None = None
    ORIGIN_AIRPORT_SEQ_ID: str | None = None
    ORIGIN_CITY_MARKET_ID: str | None = None
    ORIGIN: str | None = None
    ORIGIN_CITY_NAME: str | None = None
    ORIGIN_STATE_ABR: str | None = None
    ORIGIN_STATE_FIPS: str | None = None
    ORIGIN_STATE_NM: str | None = None
    ORIGIN_WAC: str | None = None

    DEST_AIRPORT_ID: str | None = None
    DEST_AIRPORT_SEQ_ID: str | None = None
    DEST_CITY_MARKET_ID: str | None = None
    DEST: str | None = None
    DEST_CITY_NAME: str | None = None
    DEST_STATE_ABR: str | None = None
    DEST_STATE_FIPS: str | None = None
    DEST_STATE_NM: str | None = None
    DEST_WAC: str | None = None

    CRS_DEP_TIME: str | None = None
    DEP_TIME: str | None = None
    DEP_DELAY: str | None = None
    DEP_DELAY_NEW: str | None = None
    DEP_DEL15: str | None = None
    DEP_DELAY_GROUP: str | None = None
    DEP_TIME_BLK: str | None = None
    TAXI_OUT: str | None = None
    WHEELS_OFF: str | None = None

    WHEELS_ON: str | None = None
    TAXI_IN: str | None = None
    CRS_ARR_TIME: str | None = None
    ARR_TIME: str | None = None
    ARR_DELAY: str | None = None
    ARR_DELAY_NEW: str | None = None
    ARR_DEL15: str | None = None
    ARR_DELAY_GROUP: str | None = None
    ARR_TIME_BLK: str | None = None

    CANCELLED: str | None = None
    CANCELLATION_CODE: str | None = None
    DIVERTED: str | None = None

    CRS_ELAPSED_TIME: str | None = None
    ACTUAL_ELAPSED_TIME: str | None = None
    AIR_TIME: str | None = None
    FLIGHTS: str | None = None
    DISTANCE: str | None = None
    DISTANCE_GROUP: str | None = None

    CARRIER_DELAY: str | None = None
    WEATHER_DELAY: str | None = None
    NAS_DELAY: str | None = None
    SECURITY_DELAY: str | None = None
    LATE_AIRCRAFT_DELAY: str | None = None

    FIRST_DEP_TIME: str | None = None
    TOTAL_ADD_GTIME: str | None = None
    LONGEST_ADD_GTIME: str | None = None

    DIV_AIRPORT_LANDINGS: str | None = None
    DIV_REACHED_DEST: str | None = None
    DIV_ACTUAL_ELAPSED_TIME: str | None = None
    DIV_ARR_DELAY: str | None = None
    DIV_DISTANCE: str | None = None
    DIV1_AIRPORT: str | None = None
    DIV1_AIRPORT_ID: str | None = None
    DIV1_AIRPORT_SEQ_ID: str | None = None
    DIV1_WHEELS_ON: str | None = None
    DIV1_TOTAL_GTIME: str | None = None
    DIV1_LONGEST_GTIME: str | None = None
    DIV1_WHEELS_OFF: str | None = None
    DIV1_TAIL_NUM: str | None = None
    DIV2_AIRPORT: str | None = None
    DIV2_AIRPORT_ID: str | None = None
    DIV2_AIRPORT_SEQ_ID: str | None = None
    DIV2_WHEELS_ON: str | None = None
    DIV2_TOTAL_GTIME: str | None = None
    DIV2_LONGEST_GTIME: str | None = None
    DIV2_WHEELS_OFF: str | None = None
    DIV2_TAIL_NUM: str | None = None
    DIV3_AIRPORT: str | None = None
    DIV3_AIRPORT_ID: str | None = None
    DIV3_AIRPORT_SEQ_ID: str | None = None
    DIV3_WHEELS_ON: str | None = None
    DIV3_TOTAL_GTIME: str | None = None
    DIV3_LONGEST_GTIME: str | None = None
    DIV3_WHEELS_OFF: str | None = None
    DIV3_TAIL_NUM: str | None = None
    DIV4_AIRPORT: str | None = None
    DIV4_AIRPORT_ID: str | None = None
    DIV4_AIRPORT_SEQ_ID: str | None = None
    DIV4_WHEELS_ON: str | None = None
    DIV4_TOTAL_GTIME: str | None = None
    DIV4_LONGEST_GTIME: str | None = None
    DIV4_WHEELS_OFF: str | None = None
    DIV4_TAIL_NUM: str | None = None
    DIV5_AIRPORT: str | None = None
    DIV5_AIRPORT_ID: str | None = None
    DIV5_AIRPORT_SEQ_ID: str | None = None
    DIV5_WHEELS_ON: str | None = None
    DIV5_TOTAL_GTIME: str | None = None
    DIV5_LONGEST_GTIME: str | None = None
    DIV5_WHEELS_OFF: str | None = None
    DIV5_TAIL_NUM: str | None = None
