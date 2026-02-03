from btsdatapy.core.models import LookupTable
from btsdatapy.core.utils.obfuscation import rot13


class AviationLookup(LookupTable):
    UNIQUE_CARRIERS = rot13("L_unIquE_CArrIErs")
    AIRLINE_ID = rot13("L_AIrLInE_ID")
    CARRIER_HISTORY = rot13("L_CArrIEr_HIstory")
    AIRPORT_ID = rot13("L_AIrport_ID")
    AIRPORT_SEQ_ID = rot13("L_AIrport_sEq_ID")
    CITY_MARKET_ID = rot13("L_CIty_MArKEt_ID")
    AIRPORT = rot13("L_AIrport")
    AIRPORT_STATE_ABR = rot13("L_stAtE_ABr_AvIAtIon")
    STATE_FIPS = rot13("L_stAtE_FIps")
    WORLD_AREA_CODE = rot13("L_worLD_ArEA_CoDEs")
    DELAY_GROUPS = rot13("L_ontIME_DELAy_Groups")
    DEPARTURE_TIME_BLOCK = rot13("L_DEpArrBLK")
    CANCELATION_CODES = rot13("L_CAnCELLAtIon")
    DISTANCE_GROUP = rot13("L_DIstAnCE_Group_SVQ")
    DIVERTED_LANDINGS = rot13("L_DIvErsIons")
