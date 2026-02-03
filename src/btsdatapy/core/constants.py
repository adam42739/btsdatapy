from btsdatapy.core.utils.obfuscation import rot13

BASE_URL = "https://www.transtats.bts.gov/"

ASP_DOWNLOAD_TABLE = "DL_SelectFields.aspx?"
ASP_DOWNLOAD_LOOKUP = "Download_Lookup.asp?"

ASP_TABLE_ID_PARAM = rot13("table_ID")
ASP_SH146_NAME_PARAM = rot13("DB_sh146_name")
ASP_LOOKUP_PARAM = rot13("L11k72")

USER_AGENT = "Mozilla/5.0"
CONTENT_TYPE = "application/x-www-form-urlencoded"
