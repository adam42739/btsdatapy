from btsdatapy.core.models.templates import BtsTable
from btsdatapy.core.utils.obfuscation import rot13

REPORTING_CARRIER_OTP_TABLE_ID: str = "FGJ"
REPORTING_CARRIER_OTP_SH146_NAME: str = rot13("o0-time")

MARKETING_CARRIER_OTP_TABLE_ID: str = "FGK"
MARKETING_CARRIER_OTP_SH146_NAME: str = rot13("o0-time")


class AirlineOtpTable(BtsTable):
    REPORTING_CARRIER_OTP = "reporting_carrier_otp"
    MARKETING_CARRIER_OTP = "marketing_carrier_otp"
