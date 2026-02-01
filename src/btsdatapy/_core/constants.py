from btsdatapy._core.utils.obfuscation import rot13

BASE_URL = "https://www.transtats.bts.gov/"

DOWNLOAD_ASPX = "DL_SelectFields.aspx?"

TABLE_ID_PARAM = rot13("table_ID")
SH146_NAME_PARAM = rot13("DB_sh146_name")

USER_AGENT = "Mozilla/5.0"
CONTENT_TYPE = "application/x-www-form-urlencoded"
