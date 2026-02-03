from btsdatapy.core.models.requests import BtsLookupRequest
from btsdatapy.core.models.templates import BtsLookup
from btsdatapy.core.utils.obfuscation import rot13


class AviationLookupRequest(BtsLookupRequest):
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


class AviationLookup(BtsLookup):
    UNIQUE_CARRIERS = "unique_carriers"
    AIRLINE_ID = "airline_id"
    CARRIER_HISTORY = "carrier_history"
    AIRPORT_ID = "airport_id"
    AIRPORT_SEQ_ID = "airport_seq_id"
    CITY_MARKET_ID = "city_market_id"
    AIRPORT = "airport"
    AIRPORT_STATE_ABR = "airport_state_abr"
    STATE_FIPS = "state_fips"
    WORLD_AREA_CODE = "world_area_code"
    DELAY_GROUPS = "delay_groups"
    DEPARTURE_TIME_BLOCK = "departure_time_block"
    CANCELATION_CODES = "cancelation_codes"
    DISTANCE_GROUP = "distance_group"
    DIVERTED_LANDINGS = "diverted_landings"
