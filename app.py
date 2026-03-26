import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

# ──────────────────────────────────────────────────────────────────
# PAGE CONFIG (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Eze Plumbing BOQ",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────
# PRODUCT DATABASE
# ──────────────────────────────────────────────────────────────────
HT_PRO = [
    # PIPES – HT PRO
    {"code":"5404000025-i","desc":"HT PRO S/S PIPE 250mm","cat":"PIPE","dn":"40","siz":"250mm","pr":64},
    {"code":"5405000025-i","desc":"HT PRO S/S PIPE 250mm","cat":"PIPE","dn":"50","siz":"250mm","pr":74},
    {"code":"5407500025-i","desc":"HT PRO S/S PIPE 250mm","cat":"PIPE","dn":"75","siz":"250mm","pr":122},
    {"code":"5401100025-i","desc":"HT PRO S/S PIPE 250mm","cat":"PIPE","dn":"110","siz":"250mm","pr":202},
    {"code":"5401200025-i","desc":"HT PRO S/S PIPE 250mm","cat":"PIPE","dn":"125","siz":"250mm","pr":326},
    {"code":"5401600025-i","desc":"HT PRO S/S PIPE 250mm","cat":"PIPE","dn":"160","siz":"250mm","pr":402},
    {"code":"54040050-i","desc":"HT PRO S/S PIPE 500mm","cat":"PIPE","dn":"40","siz":"500mm","pr":94},
    {"code":"54050050-i","desc":"HT PRO S/S PIPE 500mm","cat":"PIPE","dn":"50","siz":"500mm","pr":122},
    {"code":"54075050-i","desc":"HT PRO S/S PIPE 500mm","cat":"PIPE","dn":"75","siz":"500mm","pr":210},
    {"code":"540110050-i","desc":"HT PRO S/S PIPE 500mm","cat":"PIPE","dn":"110","siz":"500mm","pr":343},
    {"code":"540125050-i","desc":"HT PRO S/S PIPE 500mm","cat":"PIPE","dn":"125","siz":"500mm","pr":554},
    {"code":"540160050-i","desc":"HT PRO S/S PIPE 500mm","cat":"PIPE","dn":"160","siz":"500mm","pr":677},
    {"code":"54040100-i","desc":"HT PRO S/S PIPE 1000mm","cat":"PIPE","dn":"40","siz":"1000mm","pr":170},
    {"code":"54050100-i","desc":"HT PRO S/S PIPE 1000mm","cat":"PIPE","dn":"50","siz":"1000mm","pr":222},
    {"code":"54075100-i","desc":"HT PRO S/S PIPE 1000mm","cat":"PIPE","dn":"75","siz":"1000mm","pr":385},
    {"code":"540110100-i","desc":"HT PRO S/S PIPE 1000mm","cat":"PIPE","dn":"110","siz":"1000mm","pr":623},
    {"code":"540125100-i","desc":"HT PRO S/S PIPE 1000mm","cat":"PIPE","dn":"125","siz":"1000mm","pr":1010},
    {"code":"540160100-i","desc":"HT PRO S/S PIPE 1000mm","cat":"PIPE","dn":"160","siz":"1000mm","pr":1228},
    {"code":"54040150-i","desc":"HT PRO S/S PIPE 1500mm","cat":"PIPE","dn":"40","siz":"1500mm","pr":245},
    {"code":"54050150-i","desc":"HT PRO S/S PIPE 1500mm","cat":"PIPE","dn":"50","siz":"1500mm","pr":320},
    {"code":"54075150-i","desc":"HT PRO S/S PIPE 1500mm","cat":"PIPE","dn":"75","siz":"1500mm","pr":560},
    {"code":"540110150-i","desc":"HT PRO S/S PIPE 1500mm","cat":"PIPE","dn":"110","siz":"1500mm","pr":904},
    {"code":"540125150-i","desc":"HT PRO S/S PIPE 1500mm","cat":"PIPE","dn":"125","siz":"1500mm","pr":1466},
    {"code":"540160150-i","desc":"HT PRO S/S PIPE 1500mm","cat":"PIPE","dn":"160","siz":"1500mm","pr":1778},
    {"code":"54040200-i","desc":"HT PRO S/S PIPE 2000mm","cat":"PIPE","dn":"40","siz":"2000mm","pr":321},
    {"code":"54050200-i","desc":"HT PRO S/S PIPE 2000mm","cat":"PIPE","dn":"50","siz":"2000mm","pr":419},
    {"code":"54075200-i","desc":"HT PRO S/S PIPE 2000mm","cat":"PIPE","dn":"75","siz":"2000mm","pr":735},
    {"code":"540110200-i","desc":"HT PRO S/S PIPE 2000mm","cat":"PIPE","dn":"110","siz":"2000mm","pr":1184},
    {"code":"540125200-i","desc":"HT PRO S/S PIPE 2000mm","cat":"PIPE","dn":"125","siz":"2000mm","pr":1922},
    {"code":"540160200-i","desc":"HT PRO S/S PIPE 2000mm","cat":"PIPE","dn":"160","siz":"2000mm","pr":2330},
    {"code":"54040300-i","desc":"HT PRO S/S PIPE 3000mm","cat":"PIPE","dn":"40","siz":"3000mm","pr":472},
    {"code":"54050300-i","desc":"HT PRO S/S PIPE 3000mm","cat":"PIPE","dn":"50","siz":"3000mm","pr":616},
    {"code":"54075300-i","desc":"HT PRO S/S PIPE 3000mm","cat":"PIPE","dn":"75","siz":"3000mm","pr":1086},
    {"code":"540110300-i","desc":"HT PRO S/S PIPE 3000mm","cat":"PIPE","dn":"110","siz":"3000mm","pr":1459},
    {"code":"540125300-i","desc":"HT PRO S/S PIPE 3000mm","cat":"PIPE","dn":"125","siz":"3000mm","pr":2834},
    {"code":"540160300-i","desc":"HT PRO S/S PIPE 3000mm","cat":"PIPE","dn":"160","siz":"3000mm","pr":3430},
    {"code":"540200300-i","desc":"HT PRO S/S PIPE 3000mm","cat":"PIPE","dn":"200","siz":"3000mm","pr":6919},
    {"code":"5404040300-i","desc":"HT PRO D/S PIPE 3m","cat":"PIPE","dn":"40","siz":"3000mm DS","pr":490},
    {"code":"5405050300-i","desc":"HT PRO D/S PIPE 3m","cat":"PIPE","dn":"50","siz":"3000mm DS","pr":640},
    {"code":"5407575300-i","desc":"HT PRO D/S PIPE 3m","cat":"PIPE","dn":"75","siz":"3000mm DS","pr":1120},
    {"code":"5401111300-i","desc":"HT PRO D/S PIPE 3m","cat":"PIPE","dn":"110","siz":"3000mm DS","pr":1719},
    {"code":"5401212300-i","desc":"HT PRO D/S PIPE 3m","cat":"PIPE","dn":"125","siz":"3000mm DS","pr":2932},
    {"code":"5401616300-i","desc":"HT PRO D/S PIPE 3m","cat":"PIPE","dn":"160","siz":"3000mm DS","pr":3557},
    # BENDS
    {"code":"40040150","desc":"HT PRO BEND 15 DEG","cat":"BEND","dn":"110","siz":"-","pr":195},
    {"code":"40040350","desc":"HT PRO BEND 30 DEG","cat":"BEND","dn":"110","siz":"-","pr":199},
    {"code":"40010460","desc":"HT PRO BEND 45 DEG","cat":"BEND","dn":"40","siz":"-","pr":55},
    {"code":"40020460","desc":"HT PRO BEND 45 DEG","cat":"BEND","dn":"50","siz":"-","pr":68},
    {"code":"40030460","desc":"HT PRO BEND 45 DEG","cat":"BEND","dn":"75","siz":"-","pr":107},
    {"code":"40040460","desc":"HT PRO BEND 45 DEG","cat":"BEND","dn":"110","siz":"-","pr":155},
    {"code":"40050460","desc":"HT PRO BEND 45 DEG","cat":"BEND","dn":"125","siz":"-","pr":988},
    {"code":"40060460","desc":"HT PRO BEND 45 DEG","cat":"BEND","dn":"160","siz":"-","pr":480},
    {"code":"40010860","desc":"HT PRO BEND 87.5 DEG","cat":"BEND","dn":"40","siz":"-","pr":60},
    {"code":"40020860","desc":"HT PRO BEND 87.5 DEG","cat":"BEND","dn":"50","siz":"-","pr":64},
    {"code":"40030860","desc":"HT PRO BEND 87.5 DEG","cat":"BEND","dn":"75","siz":"-","pr":129},
    {"code":"40040860","desc":"HT PRO BEND 87.5 DEG","cat":"BEND","dn":"110","siz":"-","pr":225},
    {"code":"40050860","desc":"HT PRO BEND 87.5 DEG","cat":"BEND","dn":"125","siz":"-","pr":882},
    {"code":"40060860","desc":"HT PRO BEND 87.5 DEG","cat":"BEND","dn":"160","siz":"-","pr":602},
    # DOOR BENDS
    {"code":"40020467","desc":"HT PRO DOOR BEND 45 DEG","cat":"DOOR BEND","dn":"50","siz":"-","pr":124},
    {"code":"40040467","desc":"HT PRO DOOR BEND 45 DEG","cat":"DOOR BEND","dn":"110","siz":"-","pr":380},
    {"code":"40040468","desc":"HT PRO DOOR BEND 45 DEG (R)","cat":"DOOR BEND","dn":"110","siz":"-","pr":322},
    {"code":"40040469","desc":"HT PRO DOOR BEND 45 DEG (L)","cat":"DOOR BEND","dn":"110","siz":"-","pr":318},
    {"code":"40060457","desc":"HT PRO DOOR BEND 45 DEG","cat":"DOOR BEND","dn":"160","siz":"-","pr":1459},
    {"code":"40020867","desc":"HT PRO DOOR BEND 87.5 DEG","cat":"DOOR BEND","dn":"50","siz":"-","pr":184},
    {"code":"40030867","desc":"HT PRO DOOR BEND 87.5 DEG","cat":"DOOR BEND","dn":"75","siz":"-","pr":174},
    {"code":"40040867","desc":"HT PRO DOOR BEND 87.5 DEG","cat":"DOOR BEND","dn":"110","siz":"-","pr":431},
    {"code":"40060857","desc":"HT PRO DOOR BEND 87.5 DEG","cat":"DOOR BEND","dn":"160","siz":"-","pr":2024},
    {"code":"40040868","desc":"HT PRO DOOR BEND 87.5 DEG (R)","cat":"DOOR BEND","dn":"110","siz":"-","pr":461},
    {"code":"40040869","desc":"HT PRO DOOR BEND 87.5 DEG (L)","cat":"DOOR BEND","dn":"110","siz":"-","pr":471},
    # WYE
    {"code":"40611440","desc":"HT PRO SINGLE Y 40x40","cat":"WYE","dn":"40x40","siz":"-","pr":80},
    {"code":"40622460","desc":"HT PRO SINGLE Y 50x50","cat":"WYE","dn":"50x50","siz":"-","pr":116},
    {"code":"40633460","desc":"HT PRO SINGLE Y 75x75","cat":"WYE","dn":"75x75","siz":"-","pr":218},
    {"code":"40644460","desc":"HT PRO SINGLE Y 110x110","cat":"WYE","dn":"110x110","siz":"-","pr":479},
    {"code":"40655460","desc":"HT PRO SINGLE Y 125x125","cat":"WYE","dn":"125x125","siz":"-","pr":3736},
    {"code":"40666450","desc":"HT PRO SINGLE Y 160x160","cat":"WYE","dn":"160x160","siz":"-","pr":1618},
    {"code":"40621440","desc":"HT PRO REDUCING Y 50x40","cat":"WYE","dn":"50x40","siz":"-","pr":119},
    {"code":"40632460","desc":"HT PRO REDUCING Y 75x50","cat":"WYE","dn":"75x50","siz":"-","pr":292},
    {"code":"40642460","desc":"HT PRO REDUCING Y 110x50","cat":"WYE","dn":"110x50","siz":"-","pr":301},
    {"code":"40643460","desc":"HT PRO REDUCING Y 110x75","cat":"WYE","dn":"110x75","siz":"-","pr":482},
    {"code":"40654460","desc":"HT PRO REDUCING Y 125x110","cat":"WYE","dn":"125x110","siz":"-","pr":2518},
    {"code":"40664450","desc":"HT PRO REDUCING Y 160x110","cat":"WYE","dn":"160x110","siz":"-","pr":1889},
    {"code":"41042450","desc":"HT PRO DOUBLE Y 110x50x50","cat":"WYE","dn":"110x50x50","siz":"-","pr":1300},
    {"code":"41044450","desc":"HT PRO DOUBLE Y 110x110x110","cat":"WYE","dn":"110x110x110","siz":"-","pr":1219},
    # TEE
    {"code":"40611860","desc":"HT PRO SINGLE TEE 40x40","cat":"TEE","dn":"40x40","siz":"-","pr":92},
    {"code":"40622860","desc":"HT PRO SINGLE TEE 50x50","cat":"TEE","dn":"50x50","siz":"-","pr":101},
    {"code":"40633860","desc":"HT PRO SINGLE TEE 75x75","cat":"TEE","dn":"75x75","siz":"-","pr":164},
    {"code":"40643860-S","desc":"HT PRO SINGLE TEE 110x75","cat":"TEE","dn":"110x75","siz":"-","pr":450},
    {"code":"40655860","desc":"HT PRO SINGLE TEE 125x125","cat":"TEE","dn":"125x125","siz":"-","pr":506},
    {"code":"40666860","desc":"HT PRO SINGLE TEE 160x160","cat":"TEE","dn":"160x160","siz":"-","pr":789},
    {"code":"40621860","desc":"HT PRO REDUCING TEE 50x40","cat":"TEE","dn":"50x40","siz":"-","pr":138},
    {"code":"40632860","desc":"HT PRO REDUCING TEE 75x50","cat":"TEE","dn":"75x50","siz":"-","pr":154},
    {"code":"40642860","desc":"HT PRO REDUCING TEE 110x50","cat":"TEE","dn":"110x50","siz":"-","pr":327},
    {"code":"40652860","desc":"HT PRO REDUCING TEE 125x50","cat":"TEE","dn":"125x50","siz":"-","pr":512},
    {"code":"40664860","desc":"HT PRO REDUCING TEE 160x110","cat":"TEE","dn":"160x110","siz":"-","pr":731},
    # SWEPT TEE
    {"code":"40733860-i","desc":"HT PRO SWEPT TEE 75x75","cat":"SWEPT TEE","dn":"75x75","siz":"-","pr":217},
    {"code":"40742860-i","desc":"HT PRO SWEPT TEE 110x50","cat":"SWEPT TEE","dn":"110x50","siz":"-","pr":363},
    {"code":"40743860-i","desc":"HT PRO SWEPT TEE 110x75","cat":"SWEPT TEE","dn":"110x75","siz":"-","pr":458},
    {"code":"40744860-i","desc":"HT PRO SWEPT TEE 110x110","cat":"SWEPT TEE","dn":"110x110","siz":"-","pr":425},
    {"code":"40754860","desc":"HT PRO SWEPT TEE 125x110","cat":"SWEPT TEE","dn":"125x110","siz":"-","pr":900},
    {"code":"14040764860","desc":"HT PRO SWEPT TEE 160x110","cat":"SWEPT TEE","dn":"160x110","siz":"-","pr":1738},
    {"code":"41044860","desc":"HT PRO DOUBLE SWEPT TEE 110x110x110","cat":"SWEPT TEE","dn":"110x110x110","siz":"-","pr":1686},
    {"code":"40733867-i","desc":"HT PRO DOOR SWEPT TEE 75x75","cat":"SWEPT TEE","dn":"75x75","siz":"-","pr":383},
    {"code":"40742867-i","desc":"HT PRO DOOR SWEPT TEE 110x50","cat":"SWEPT TEE","dn":"110x50","siz":"-","pr":513},
    {"code":"40743867-i","desc":"HT PRO DOOR SWEPT TEE 110x75","cat":"SWEPT TEE","dn":"110x75","siz":"-","pr":610},
    {"code":"40744867-i","desc":"HT PRO DOOR SWEPT TEE 110x110","cat":"SWEPT TEE","dn":"110x110","siz":"-","pr":628},
    {"code":"40664857-i","desc":"HT PRO DOOR SWEPT TEE 160x110","cat":"SWEPT TEE","dn":"160x110","siz":"-","pr":2305},
    # TRAP / MFT
    {"code":"49540750 G-i","desc":"HT PRO P TRAP 110x110","cat":"TRAP","dn":"110x110","siz":"-","pr":943},
    {"code":"41840051-i","desc":"HT PRO S TRAP 110x110","cat":"TRAP","dn":"110x110","siz":"-","pr":1885},
    {"code":"69111750 G-i","desc":"HT PRO NAHANI TRAP 110x75","cat":"TRAP","dn":"110x75","siz":"-","pr":541},
    {"code":"60117051","desc":"HT PRO MFT 110x75x50","cat":"MFT","dn":"110x75x50","siz":"-","pr":1047},
    {"code":"14048111060 G-i","desc":"HT PRO MFT SOCKETED 110x75x50","cat":"MFT","dn":"110x75x50","siz":"-","pr":1400},
    # SPECIAL
    {"code":"69201551 G-i","desc":"HT PRO HEIGHT RISER L150","cat":"SPECIAL","dn":"110","siz":"-","pr":414},
    {"code":"69203551 G-i","desc":"HT PRO HEIGHT RISER L350","cat":"SPECIAL","dn":"110","siz":"-","pr":614},
    {"code":"4049911100 G-i","desc":"HT PRO H.A.F.F STACK","cat":"SPECIAL","dn":"110x110x75","siz":"-","pr":5500},
    {"code":"49130060","desc":"HT PRO CLEANING PIPE DN75","cat":"INSPECTION","dn":"75","siz":"-","pr":383},
    {"code":"49140060","desc":"HT PRO CLEANING PIPE DN110","cat":"INSPECTION","dn":"110","siz":"-","pr":472},
    {"code":"49150060","desc":"HT PRO CLEANING PIPE DN125","cat":"INSPECTION","dn":"125","siz":"-","pr":1041},
    {"code":"49160060","desc":"HT PRO CLEANING PIPE DN160","cat":"INSPECTION","dn":"160","siz":"-","pr":999},
    {"code":"41244850","desc":"HT PRO CORNER BRANCH 110x110x110","cat":"SPECIAL","dn":"110x110x110","siz":"-","pr":1122},
    # COUPLER
    {"code":"41710050","desc":"HT PRO COUPLER DN40","cat":"COUPLER","dn":"40","siz":"-","pr":61},
    {"code":"41720055","desc":"HT PRO COUPLER DN50","cat":"COUPLER","dn":"50","siz":"-","pr":71},
    {"code":"41730050","desc":"HT PRO COUPLER DN75","cat":"COUPLER","dn":"75","siz":"-","pr":96},
    {"code":"41740250","desc":"HT PRO COUPLER DN110","cat":"COUPLER","dn":"110","siz":"-","pr":175},
    {"code":"41750065","desc":"HT PRO COUPLER DN125","cat":"COUPLER","dn":"125","siz":"-","pr":412},
    {"code":"41760055","desc":"HT PRO COUPLER DN160","cat":"COUPLER","dn":"160","siz":"-","pr":878},
    {"code":"41720053","desc":"HT PRO REPAIR COUPLER DN50","cat":"COUPLER","dn":"50","siz":"-","pr":96},
    {"code":"41730053","desc":"HT PRO REPAIR COUPLER DN75","cat":"COUPLER","dn":"75","siz":"-","pr":107},
    {"code":"41740053","desc":"HT PRO REPAIR COUPLER DN110","cat":"COUPLER","dn":"110","siz":"-","pr":179},
    # REDUCER
    {"code":"42121060","desc":"HT PRO REDUCER 50x40","cat":"REDUCER","dn":"50x40","siz":"-","pr":55},
    {"code":"42132050","desc":"HT PRO REDUCER 75x50","cat":"REDUCER","dn":"75x50","siz":"-","pr":69},
    {"code":"42142050","desc":"HT PRO REDUCER 110x50","cat":"REDUCER","dn":"110x50","siz":"-","pr":152},
    {"code":"42143050","desc":"HT PRO REDUCER 110x75","cat":"REDUCER","dn":"110x75","siz":"-","pr":179},
    {"code":"42154060","desc":"HT PRO REDUCER 125x110","cat":"REDUCER","dn":"125x110","siz":"-","pr":351},
    {"code":"42164050","desc":"HT PRO REDUCER 160x110","cat":"REDUCER","dn":"160x110","siz":"-","pr":544},
    {"code":"P0500000000040K","desc":"HT PRO CONCENTRIC REDUCER 50x40","cat":"REDUCER","dn":"50x40","siz":"-","pr":160},
    {"code":"P07500000050K","desc":"HT PRO CONCENTRIC REDUCER 75x50","cat":"REDUCER","dn":"75x50","siz":"-","pr":211},
    {"code":"P1100000000050V","desc":"HT PRO CONCENTRIC REDUCER 110x50","cat":"REDUCER","dn":"110x50","siz":"-","pr":273},
    {"code":"P1100000000075V","desc":"HT PRO CONCENTRIC REDUCER 110x75","cat":"REDUCER","dn":"110x75","siz":"-","pr":334},
    # END CAP / VENT
    {"code":"41610040","desc":"HT PRO END CAP DN40","cat":"END CAP","dn":"40","siz":"-","pr":29},
    {"code":"41620050","desc":"HT PRO END CAP DN50","cat":"END CAP","dn":"50","siz":"-","pr":55},
    {"code":"41630050","desc":"HT PRO END CAP DN75","cat":"END CAP","dn":"75","siz":"-","pr":58},
    {"code":"41640050","desc":"HT PRO END CAP DN110","cat":"END CAP","dn":"110","siz":"-","pr":96},
    {"code":"41650060","desc":"HT PRO END CAP DN125","cat":"END CAP","dn":"125","siz":"-","pr":209},
    {"code":"41660060","desc":"HT PRO END CAP DN160","cat":"END CAP","dn":"160","siz":"-","pr":287},
    {"code":"4042320040","desc":"HT PRO VENT COWL DN50","cat":"VENT COWL","dn":"50","siz":"-","pr":199},
    {"code":"4042330040","desc":"HT PRO VENT COWL DN75","cat":"VENT COWL","dn":"75","siz":"-","pr":154},
    {"code":"4042340060","desc":"HT PRO VENT COWL DN110","cat":"VENT COWL","dn":"110","siz":"-","pr":162},
    {"code":"4042360040","desc":"HT PRO VENT COWL DN160","cat":"VENT COWL","dn":"160","siz":"-","pr":344},
    # CLAMP
    {"code":"48100040","desc":"HT PRO CLAMP DN40","cat":"CLAMP","dn":"40","siz":"-","pr":105},
    {"code":"48100050","desc":"HT PRO CLAMP DN50","cat":"CLAMP","dn":"50","siz":"-","pr":115},
    {"code":"48100075","desc":"HT PRO CLAMP DN75","cat":"CLAMP","dn":"75","siz":"-","pr":145},
    {"code":"48100011","desc":"HT PRO CLAMP DN110","cat":"CLAMP","dn":"110","siz":"-","pr":175},
    {"code":"48100012","desc":"HT PRO CLAMP DN125","cat":"CLAMP","dn":"125","siz":"-","pr":205},
    {"code":"48100016","desc":"HT PRO CLAMP DN160","cat":"CLAMP","dn":"160","siz":"-","pr":250},
    {"code":"48100020","desc":"HT PRO CLAMP DN200","cat":"CLAMP","dn":"200","siz":"-","pr":295},
    # WC CONNECTOR
    {"code":"41540020","desc":"STRAIGHT WC CONNECTOR","cat":"WC CONN","dn":"110","siz":"-","pr":1298},
    {"code":"41540027","desc":"DOOR STRAIGHT WC CONNECTOR (INSP)","cat":"WC CONN","dn":"110","siz":"-","pr":1480},
    {"code":"41542866","desc":"WC BEND WITH DOOR INSPECTION","cat":"WC CONN","dn":"110","siz":"-","pr":1299},
    {"code":"41540615","desc":"FLANGE FOR WC BEND - WHITE","cat":"WC CONN","dn":"110","siz":"-","pr":55},
    {"code":"47700012","desc":"LUBRICANT TIN 250ML","cat":"ACCESSORIES","dn":"-","siz":"-","pr":165},
]

ULTRA_SILENT = [
    # PIPES – ULTRA SILENT
    {"code":"5753200300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"32","siz":"3000mm","pr":790},
    {"code":"5754000025-i","desc":"US S/S PIPE 250mm","cat":"PIPE","dn":"40","siz":"250mm","pr":97},
    {"code":"5755000025-i","desc":"US S/S PIPE 250mm","cat":"PIPE","dn":"50","siz":"250mm","pr":126},
    {"code":"5757500025-i","desc":"US S/S PIPE 250mm","cat":"PIPE","dn":"75","siz":"250mm","pr":231},
    {"code":"5751100025-i","desc":"US S/S PIPE 250mm","cat":"PIPE","dn":"110","siz":"250mm","pr":313},
    {"code":"5751200025-i","desc":"US S/S PIPE 250mm","cat":"PIPE","dn":"125","siz":"250mm","pr":392},
    {"code":"5751600025-i","desc":"US S/S PIPE 250mm","cat":"PIPE","dn":"160","siz":"250mm","pr":617},
    {"code":"5754000050-i","desc":"US S/S PIPE 500mm","cat":"PIPE","dn":"40","siz":"500mm","pr":166},
    {"code":"5755000050-i","desc":"US S/S PIPE 500mm","cat":"PIPE","dn":"50","siz":"500mm","pr":214},
    {"code":"5757500050-i","desc":"US S/S PIPE 500mm","cat":"PIPE","dn":"75","siz":"500mm","pr":402},
    {"code":"5751100050-i","desc":"US S/S PIPE 500mm","cat":"PIPE","dn":"110","siz":"500mm","pr":542},
    {"code":"5751200050-i","desc":"US S/S PIPE 500mm","cat":"PIPE","dn":"125","siz":"500mm","pr":672},
    {"code":"5751600050-i","desc":"US S/S PIPE 500mm","cat":"PIPE","dn":"160","siz":"500mm","pr":1062},
    {"code":"5754000100-i","desc":"US S/S PIPE 1000mm","cat":"PIPE","dn":"40","siz":"1000mm","pr":305},
    {"code":"5755000100-i","desc":"US S/S PIPE 1000mm","cat":"PIPE","dn":"50","siz":"1000mm","pr":390},
    {"code":"5757500100-i","desc":"US S/S PIPE 1000mm","cat":"PIPE","dn":"75","siz":"1000mm","pr":742},
    {"code":"5751100100-i","desc":"US S/S PIPE 1000mm","cat":"PIPE","dn":"110","siz":"1000mm","pr":1001},
    {"code":"5751200100-i","desc":"US S/S PIPE 1000mm","cat":"PIPE","dn":"125","siz":"1000mm","pr":1232},
    {"code":"5751600100-i","desc":"US S/S PIPE 1000mm","cat":"PIPE","dn":"160","siz":"1000mm","pr":1950},
    {"code":"5752000100-i","desc":"US S/S PIPE 1000mm","cat":"PIPE","dn":"200","siz":"1000mm","pr":2438},
    {"code":"5754000150-i","desc":"US S/S PIPE 1500mm","cat":"PIPE","dn":"40","siz":"1500mm","pr":442},
    {"code":"5755000150-i","desc":"US S/S PIPE 1500mm","cat":"PIPE","dn":"50","siz":"1500mm","pr":566},
    {"code":"5757500150-i","desc":"US S/S PIPE 1500mm","cat":"PIPE","dn":"75","siz":"1500mm","pr":1081},
    {"code":"5751100150-i","desc":"US S/S PIPE 1500mm","cat":"PIPE","dn":"110","siz":"1500mm","pr":1459},
    {"code":"5751200150-i","desc":"US S/S PIPE 1500mm","cat":"PIPE","dn":"125","siz":"1500mm","pr":1992},
    {"code":"5751600150-i","desc":"US S/S PIPE 1500mm","cat":"PIPE","dn":"160","siz":"1500mm","pr":2839},
    {"code":"5754000200-i","desc":"US S/S PIPE 2000mm","cat":"PIPE","dn":"40","siz":"2000mm","pr":581},
    {"code":"5755000200-i","desc":"US S/S PIPE 2000mm","cat":"PIPE","dn":"50","siz":"2000mm","pr":742},
    {"code":"5757500200-i","desc":"US S/S PIPE 2000mm","cat":"PIPE","dn":"75","siz":"2000mm","pr":1421},
    {"code":"5751100200-i","desc":"US S/S PIPE 2000mm","cat":"PIPE","dn":"110","siz":"2000mm","pr":1917},
    {"code":"5751200200-i","desc":"US S/S PIPE 2000mm","cat":"PIPE","dn":"125","siz":"2000mm","pr":2351},
    {"code":"5751600200-i","desc":"US S/S PIPE 2000mm","cat":"PIPE","dn":"160","siz":"2000mm","pr":3727},
    {"code":"5754000300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"40","siz":"3000mm","pr":856},
    {"code":"5755000300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"50","siz":"3000mm","pr":1094},
    {"code":"5757500300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"75","siz":"3000mm","pr":2101},
    {"code":"5751100300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"110","siz":"3000mm","pr":2461},
    {"code":"5751200300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"125","siz":"3000mm","pr":3471},
    {"code":"5751600300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"160","siz":"3000mm","pr":5050},
    {"code":"5752000300-i","desc":"US S/S PIPE 3m","cat":"PIPE","dn":"200","siz":"3000mm","pr":7100},
    {"code":"5754040300-i","desc":"US D/S PIPE 3m","cat":"PIPE","dn":"40","siz":"3000mm DS","pr":884},
    {"code":"5755050300-i","desc":"US D/S PIPE 3m","cat":"PIPE","dn":"50","siz":"3000mm DS","pr":1132},
    {"code":"5757575300-i","desc":"US D/S PIPE 3m","cat":"PIPE","dn":"75","siz":"3000mm DS","pr":2161},
    {"code":"5751111300-i","desc":"US D/S PIPE 3m","cat":"PIPE","dn":"110","siz":"3000mm DS","pr":2592},
    {"code":"5751212300-i","desc":"US D/S PIPE 3m","cat":"PIPE","dn":"125","siz":"3000mm DS","pr":3583},
    {"code":"5751616300-i","desc":"US D/S PIPE 3m","cat":"PIPE","dn":"160","siz":"3000mm DS","pr":5677},
    # BENDS
    {"code":"7070010170","desc":"US BEND 15 DEG","cat":"BEND","dn":"40","siz":"-","pr":68},
    {"code":"7070020170","desc":"US BEND 15 DEG","cat":"BEND","dn":"50","siz":"-","pr":85},
    {"code":"7070030170","desc":"US BEND 15 DEG","cat":"BEND","dn":"75","siz":"-","pr":153},
    {"code":"7070040170","desc":"US BEND 15 DEG","cat":"BEND","dn":"110","siz":"-","pr":582},
    {"code":"7070050170","desc":"US BEND 15 DEG","cat":"BEND","dn":"125","siz":"-","pr":578},
    {"code":"7070060170","desc":"US BEND 15 DEG","cat":"BEND","dn":"160","siz":"-","pr":1131},
    {"code":"7070010370","desc":"US BEND 30 DEG","cat":"BEND","dn":"40","siz":"-","pr":85},
    {"code":"7070020370","desc":"US BEND 30 DEG","cat":"BEND","dn":"50","siz":"-","pr":85},
    {"code":"7070030370","desc":"US BEND 30 DEG","cat":"BEND","dn":"75","siz":"-","pr":171},
    {"code":"7070040370","desc":"US BEND 30 DEG","cat":"BEND","dn":"110","siz":"-","pr":606},
    {"code":"7070010470","desc":"US BEND 45 DEG","cat":"BEND","dn":"40","siz":"-","pr":68},
    {"code":"7070020470","desc":"US BEND 45 DEG","cat":"BEND","dn":"50","siz":"-","pr":102},
    {"code":"7070030470","desc":"US BEND 45 DEG","cat":"BEND","dn":"75","siz":"-","pr":171},
    {"code":"7070040470","desc":"US BEND 45 DEG","cat":"BEND","dn":"110","siz":"-","pr":534},
    {"code":"7070050470","desc":"US BEND 45 DEG","cat":"BEND","dn":"125","siz":"-","pr":749},
    {"code":"7070060470","desc":"US BEND 45 DEG","cat":"BEND","dn":"160","siz":"-","pr":1002},
    {"code":"7070080470","desc":"US BEND 45 DEG","cat":"BEND","dn":"200","siz":"-","pr":2911},
    {"code":"7070010870","desc":"US BEND 87.5 DEG","cat":"BEND","dn":"40","siz":"-","pr":85},
    {"code":"7070020870","desc":"US BEND 87.5 DEG","cat":"BEND","dn":"50","siz":"-","pr":102},
    {"code":"7070030870","desc":"US BEND 87.5 DEG","cat":"BEND","dn":"75","siz":"-","pr":202},
    {"code":"7070040870","desc":"US BEND 87.5 DEG","cat":"BEND","dn":"110","siz":"-","pr":627},
    {"code":"7070050870","desc":"US BEND 87.5 DEG","cat":"BEND","dn":"125","siz":"-","pr":833},
    {"code":"7070060870","desc":"US BEND 87.5 DEG","cat":"BEND","dn":"160","siz":"-","pr":1395},
    # WYE
    {"code":"7074010470","desc":"US SINGLE Y 40x40","cat":"WYE","dn":"40x40","siz":"-","pr":296},
    {"code":"7074020470","desc":"US SINGLE Y 50x50","cat":"WYE","dn":"50x50","siz":"-","pr":342},
    {"code":"7074030470","desc":"US SINGLE Y 75x75","cat":"WYE","dn":"75x75","siz":"-","pr":704},
    {"code":"7074040470","desc":"US SINGLE Y 110x110","cat":"WYE","dn":"110x110","siz":"-","pr":1399},
    {"code":"7074050470","desc":"US SINGLE Y 125x125","cat":"WYE","dn":"125x125","siz":"-","pr":2020},
    {"code":"7074060470","desc":"US SINGLE Y 160x160","cat":"WYE","dn":"160x160","siz":"-","pr":3428},
    {"code":"7074021470","desc":"US REDUCING Y 50x40","cat":"WYE","dn":"50x40","siz":"-","pr":342},
    {"code":"7074032470","desc":"US REDUCING Y 75x50","cat":"WYE","dn":"75x50","siz":"-","pr":647},
    {"code":"7074042470","desc":"US REDUCING Y 110x50","cat":"WYE","dn":"110x50","siz":"-","pr":1194},
    {"code":"7074043470","desc":"US REDUCING Y 110x75","cat":"WYE","dn":"110x75","siz":"-","pr":1281},
    {"code":"7074054470","desc":"US REDUCING Y 125x110","cat":"WYE","dn":"125x110","siz":"-","pr":1912},
    {"code":"7074064470","desc":"US REDUCING Y 160x110","cat":"WYE","dn":"160x110","siz":"-","pr":3124},
    # SWEPT TEE
    {"code":"7074010870","desc":"US SWEPT TEE 40x40","cat":"SWEPT TEE","dn":"40x40","siz":"-","pr":330},
    {"code":"7074020870","desc":"US SWEPT TEE 50x50","cat":"SWEPT TEE","dn":"50x50","siz":"-","pr":398},
    {"code":"7074030870","desc":"US SWEPT TEE 75x75","cat":"SWEPT TEE","dn":"75x75","siz":"-","pr":793},
    {"code":"7074040870","desc":"US SWEPT TEE 110x110","cat":"SWEPT TEE","dn":"110x110","siz":"-","pr":1574},
    {"code":"7074050870","desc":"US SWEPT TEE 125x125","cat":"SWEPT TEE","dn":"125x125","siz":"-","pr":2273},
    {"code":"7074060870","desc":"US SWEPT TEE 160x160","cat":"SWEPT TEE","dn":"160x160","siz":"-","pr":3856},
    {"code":"7074042870","desc":"US REDUCING SWEPT TEE 110x50","cat":"SWEPT TEE","dn":"110x50","siz":"-","pr":1313},
    {"code":"7074043870","desc":"US REDUCING SWEPT TEE 110x75","cat":"SWEPT TEE","dn":"110x75","siz":"-","pr":1394},
    {"code":"7074054870","desc":"US REDUCING SWEPT TEE 125x110","cat":"SWEPT TEE","dn":"125x110","siz":"-","pr":2154},
    {"code":"7074064870","desc":"US REDUCING SWEPT TEE 160x110","cat":"SWEPT TEE","dn":"160x110","siz":"-","pr":3512},
    # TRAP / MFT
    {"code":"49540750 B-i","desc":"US P TRAP 110x110","cat":"TRAP","dn":"110x110","siz":"-","pr":1196},
    {"code":"7071840070 B-i","desc":"US S TRAP 110x110","cat":"TRAP","dn":"110x110","siz":"-","pr":2392},
    {"code":"69111750 B-i","desc":"US NAHANI TRAP 110x75","cat":"TRAP","dn":"110x75","siz":"-","pr":651},
    {"code":"60117060","desc":"US MFT W/O RING 110x75x50","cat":"MFT","dn":"110x75x50","siz":"-","pr":1247},
    {"code":"S11050505075","desc":"US MFT WITH RING 110x75x50","cat":"MFT","dn":"110x75x50","siz":"-","pr":1482},
    {"code":"17078111070 B-i","desc":"US MFT WITH SOCKET 110x75x50","cat":"MFT","dn":"110x75x50","siz":"-","pr":1529},
    # COUPLER
    {"code":"7071710270","desc":"US DOUBLE SOCKET DN40","cat":"COUPLER","dn":"40","siz":"-","pr":161},
    {"code":"7071720275","desc":"US ONE WAY SOCKET DN50","cat":"COUPLER","dn":"50","siz":"-","pr":162},
    {"code":"7071730275","desc":"US ONE WAY SOCKET DN75","cat":"COUPLER","dn":"75","siz":"-","pr":293},
    {"code":"7071740275","desc":"US ONE WAY SOCKET DN110","cat":"COUPLER","dn":"110","siz":"-","pr":533},
    {"code":"7071750275","desc":"US ONE WAY SOCKET DN125","cat":"COUPLER","dn":"125","siz":"-","pr":732},
    {"code":"7071760275","desc":"US ONE WAY SOCKET DN160","cat":"COUPLER","dn":"160","siz":"-","pr":1431},
    {"code":"7071780275","desc":"US ONE WAY SOCKET DN200","cat":"COUPLER","dn":"200","siz":"-","pr":2162},
    # REDUCER
    {"code":"7072121070","desc":"US REDUCER 50x40","cat":"REDUCER","dn":"50x40","siz":"-","pr":332},
    {"code":"7072132070","desc":"US REDUCER 75x50","cat":"REDUCER","dn":"75x50","siz":"-","pr":355},
    {"code":"7072142070","desc":"US REDUCER 110x50","cat":"REDUCER","dn":"110x50","siz":"-","pr":391},
    {"code":"7072143070","desc":"US REDUCER 110x75","cat":"REDUCER","dn":"110x75","siz":"-","pr":409},
    {"code":"7072154070","desc":"US REDUCER 125x110","cat":"REDUCER","dn":"125x110","siz":"-","pr":511},
    {"code":"7072164070","desc":"US REDUCER 160x110","cat":"REDUCER","dn":"160x110","siz":"-","pr":851},
    {"code":"7072165070","desc":"US REDUCER 160x125","cat":"REDUCER","dn":"160x125","siz":"-","pr":969},
    # END CAP / VENT
    {"code":"7071610070","desc":"US END CAP DN40","cat":"END CAP","dn":"40","siz":"-","pr":33},
    {"code":"7071620070","desc":"US END CAP DN50","cat":"END CAP","dn":"50","siz":"-","pr":65},
    {"code":"7071630070","desc":"US END CAP DN75","cat":"END CAP","dn":"75","siz":"-","pr":131},
    {"code":"7071640070","desc":"US END CAP DN110","cat":"END CAP","dn":"110","siz":"-","pr":293},
    {"code":"7071650070","desc":"US END CAP DN125","cat":"END CAP","dn":"125","siz":"-","pr":631},
    {"code":"7071660070","desc":"US END CAP DN160","cat":"END CAP","dn":"160","siz":"-","pr":640},
    {"code":"42320040","desc":"US VENT CAP DN50","cat":"VENT COWL","dn":"50","siz":"-","pr":199},
    {"code":"42330040","desc":"US VENT CAP DN75","cat":"VENT COWL","dn":"75","siz":"-","pr":154},
    {"code":"42340060","desc":"US VENT CAP DN110","cat":"VENT COWL","dn":"110","siz":"-","pr":162},
    {"code":"42360040","desc":"US VENT CAP DN160","cat":"VENT COWL","dn":"160","siz":"-","pr":344},
    # CLAMP
    {"code":"7890004070","desc":"US HD SPLIT CLAMP DN40","cat":"CLAMP","dn":"40","siz":"-","pr":190},
    {"code":"7890005070","desc":"US HD SPLIT CLAMP DN50","cat":"CLAMP","dn":"50","siz":"-","pr":215},
    {"code":"7890007570","desc":"US HD SPLIT CLAMP DN75","cat":"CLAMP","dn":"75","siz":"-","pr":260},
    {"code":"7890011070","desc":"US HD SPLIT CLAMP DN110","cat":"CLAMP","dn":"110","siz":"-","pr":340},
    {"code":"7890012570","desc":"US HD SPLIT CLAMP DN125","cat":"CLAMP","dn":"125","siz":"-","pr":360},
    {"code":"7890016070","desc":"US HD SPLIT CLAMP DN160","cat":"CLAMP","dn":"160","siz":"-","pr":450},
    {"code":"7890020070","desc":"US HD SPLIT CLAMP DN200","cat":"CLAMP","dn":"200","siz":"-","pr":525},
    # SPECIAL
    {"code":"69201551 B-i","desc":"US HEIGHT RISER L150","cat":"SPECIAL","dn":"110","siz":"-","pr":542},
    {"code":"69203551 B-i","desc":"US HEIGHT RISER L350","cat":"SPECIAL","dn":"110","siz":"-","pr":814},
    {"code":"7079911100 B-i","desc":"US H.A.F.F STACK 110x110x75","cat":"SPECIAL","dn":"110x110x75","siz":"-","pr":7500},
    {"code":"70114500","desc":"SMARTLOCK TRAP 140/50","cat":"SPECIAL","dn":"50","siz":"-","pr":1036},
    {"code":"7072330000","desc":"US LOCK SEAL DN75","cat":"SPECIAL","dn":"75","siz":"-","pr":362},
    {"code":"7072340000","desc":"US LOCK SEAL DN110","cat":"SPECIAL","dn":"110","siz":"-","pr":804},
    {"code":"7078004000","desc":"US END LOCK DN110","cat":"SPECIAL","dn":"110","siz":"-","pr":1265},
    {"code":"7981100000","desc":"US ULTRA SEAL DN110","cat":"SPECIAL","dn":"110","siz":"-","pr":1796},
    # WC CONNECTOR
    {"code":"41540020-US","desc":"STRAIGHT WC CONNECTOR","cat":"WC CONN","dn":"110","siz":"-","pr":1298},
    {"code":"41540027-US","desc":"DOOR WC CONNECTOR WITH INSP.","cat":"WC CONN","dn":"110","siz":"-","pr":1480},
    {"code":"41542866-US","desc":"WC CONNECTOR BEND WITH INSP.","cat":"WC CONN","dn":"110","siz":"-","pr":1299},
    {"code":"47700012-US","desc":"LUBRICANT 250 ML","cat":"ACCESSORIES","dn":"-","siz":"-","pr":165},
]

# Build full dataset
ALL_PRODUCTS = (
    [dict(p, series="HT Pro") for p in HT_PRO] +
    [dict(p, series="Ultra Silent") for p in ULTRA_SILENT]
)

PIPE_DNS = ["32", "40", "50", "63", "75", "90", "110", "125", "160", "200"]

FITTING_CATS = [
    {"key": "BEND",        "label": "🔄 BENDS",        "emoji": "🔄"},
    {"key": "DOOR BEND",   "label": "🚪 DOOR BENDS",   "emoji": "🚪"},
    {"key": "WYE",         "label": "⑂ WYE / Y",       "emoji": "⑂"},
    {"key": "TEE",         "label": "⊤ TEES",          "emoji": "⊤"},
    {"key": "SWEPT TEE",   "label": "↪ SWEPT TEE",     "emoji": "↪"},
    {"key": "TRAP",        "label": "∪ TRAPS",         "emoji": "∪"},
    {"key": "MFT",         "label": "⊞ MFT",           "emoji": "⊞"},
    {"key": "INSPECTION",  "label": "🔍 INSPECTION",   "emoji": "🔍"},
    {"key": "COUPLER",     "label": "○ COUPLERS",      "emoji": "○"},
    {"key": "REDUCER",     "label": "⊃ REDUCERS",      "emoji": "⊃"},
    {"key": "END CAP",     "label": "◼ END CAPS",      "emoji": "◼"},
    {"key": "VENT COWL",   "label": "↑ VENT COWL",     "emoji": "↑"},
    {"key": "CLAMP",       "label": "🗜 CLAMPS",        "emoji": "🗜"},
    {"key": "WC CONN",     "label": "⊕ WC CONN.",      "emoji": "⊕"},
    {"key": "SPECIAL",     "label": "★ SPECIAL",       "emoji": "★"},
    {"key": "ACCESSORIES", "label": "🔧 ACCESSORIES",  "emoji": "🔧"},
]


# ──────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "boq": {},           # {code: {product_dict + qty}}
        "active_pipe_dn": None,
        "active_fit_cat": None,
        "series_filter": "Both",
        "project_name": "",
        "contractor": "",
        "project_date": str(date.today()),
        "discount": 0,
        "gst_pct": 18,
        "incl_gst": False,
        "active_tab": "Dashboard",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ──────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────
def get_pool():
    sf = st.session_state.series_filter
    if sf == "HT Pro":
        return [p for p in ALL_PRODUCTS if p["series"] == "HT Pro"]
    elif sf == "Ultra Silent":
        return [p for p in ALL_PRODUCTS if p["series"] == "Ultra Silent"]
    return ALL_PRODUCTS


def add_to_boq(product):
    code = product["code"]
    if code in st.session_state.boq:
        st.session_state.boq[code]["qty"] += 1
    else:
        st.session_state.boq[code] = dict(product, qty=1)


def boq_totals():
    items = list(st.session_state.boq.values())
    gross = sum(i["pr"] * i["qty"] for i in items)
    disc_amt = gross * st.session_state.discount / 100
    net = gross - disc_amt
    gst_amt = net * st.session_state.gst_pct / 100 if st.session_state.incl_gst else 0
    grand = net + gst_amt
    total_qty = sum(i["qty"] for i in items)
    return gross, disc_amt, net, gst_amt, grand, total_qty


def to_excel_bytes():
    items = list(st.session_state.boq.values())
    gross, disc_amt, net, gst_amt, grand, total_qty = boq_totals()
    rows = []
    for idx, item in enumerate(items, 1):
        rows.append({
            "Sr.": idx,
            "Series": item["series"],
            "Item Code": item["code"],
            "Description": item["desc"],
            "DN": item["dn"],
            "Size": item["siz"] if item["siz"] != "-" else "",
            "Unit Price (Rs)": item["pr"],
            "Qty": item["qty"],
            "Amount (Rs)": item["pr"] * item["qty"],
        })

    summary_rows = [
        {"Description": "", "Amount (Rs)": ""},
        {"Description": f"Project: {st.session_state.project_name}", "Amount (Rs)": ""},
        {"Description": f"Contractor: {st.session_state.contractor}", "Amount (Rs)": ""},
        {"Description": f"Date: {st.session_state.project_date}", "Amount (Rs)": ""},
        {"Description": "", "Amount (Rs)": ""},
        {"Description": "Gross Total (Ex-GST)", "Amount (Rs)": gross},
    ]
    if st.session_state.discount > 0:
        summary_rows.append({"Description": f"Discount @ {st.session_state.discount}%", "Amount (Rs)": -round(disc_amt)})
        summary_rows.append({"Description": "Net Total (Ex-GST)", "Amount (Rs)": round(net)})
    if st.session_state.incl_gst:
        summary_rows.append({"Description": f"GST @ {st.session_state.gst_pct}%", "Amount (Rs)": round(gst_amt)})
    summary_rows.append({"Description": "GRAND TOTAL", "Amount (Rs)": round(grand)})

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_boq = pd.DataFrame(rows)
        df_boq.to_excel(writer, sheet_name="BOQ", index=False)
        df_sum = pd.DataFrame(summary_rows)
        df_sum.to_excel(writer, sheet_name="Summary", index=False)

        # Style BOQ sheet
        ws = writer.sheets["BOQ"]
        col_widths = [5, 14, 24, 44, 12, 12, 16, 8, 16]
        for i, w in enumerate(col_widths, 1):
            ws.column_dimensions[ws.cell(1, i).column_letter].width = w

    return output.getvalue()


def import_from_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        required = {"Item Code", "Qty"}
        if not required.issubset(set(df.columns)):
            return False, "Missing columns: Item Code, Qty"
        code_map = {p["code"]: p for p in ALL_PRODUCTS}
        count = 0
        new_boq = {}
        for _, row in df.iterrows():
            code = str(row.get("Item Code", "")).strip()
            qty = int(row.get("Qty", 0)) if pd.notna(row.get("Qty", 0)) else 0
            if code and qty > 0 and code in code_map:
                new_boq[code] = dict(code_map[code], qty=qty)
                count += 1
        if count > 0:
            st.session_state.boq = new_boq
            return True, f"Imported {count} items successfully!"
        return False, "No matching items found in file."
    except Exception as e:
        return False, f"Error reading file: {e}"


# ──────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── global ── */
[data-testid="stAppViewContainer"] { background: #0a0e1a; }
[data-testid="stHeader"] { background: #0a0e1a; border-bottom: 1px solid #1e293b; }
.block-container { padding: 1rem 1.5rem 4rem !important; max-width: 1400px; }

/* ── tile buttons ── */
div.stButton > button {
    width: 100%; border-radius: 10px; font-weight: 700;
    transition: all 0.2s; border: 2px solid #334155;
    background: #1e293b; color: #e2e8f0;
    padding: 0.6rem 0.4rem;
}
div.stButton > button:hover {
    border-color: #3b82f6; background: #1e3a5f; color: #93c5fd;
    transform: translateY(-2px); box-shadow: 0 4px 16px #3b82f640;
}
div.stButton > button:active { transform: scale(0.98); }

/* ── metric cards ── */
[data-testid="metric-container"] {
    background: #1e293b; border-radius: 10px;
    padding: 0.75rem 1rem; border: 1px solid #334155;
}
[data-testid="stMetricLabel"] { font-size: 12px; color: #64748b; }
[data-testid="stMetricValue"] { font-size: 20px; color: #34d399; font-weight: 800; }

/* ── section headings ── */
.section-head {
    background: linear-gradient(90deg, #1e3a5f, #0a0e1a);
    border-left: 4px solid #3b82f6; border-radius: 4px;
    padding: 8px 14px; margin-bottom: 12px;
    color: #93c5fd; font-weight: 700; font-size: 15px;
}
.fit-head {
    background: linear-gradient(90deg, #3d2000, #0a0e1a);
    border-left: 4px solid #f59e0b;
}

/* ── product cards ── */
.prod-card {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 8px; padding: 10px 12px; margin-bottom: 6px;
    display: flex; justify-content: space-between; align-items: center;
}
.ht-badge {
    background: #7c2d12; color: #fdba74;
    font-size: 10px; font-weight: 700; padding: 2px 7px;
    border-radius: 4px; display: inline-block;
}
.us-badge {
    background: #1e3a5f; color: #7dd3fc;
    font-size: 10px; font-weight: 700; padding: 2px 7px;
    border-radius: 4px; display: inline-block;
}
.price-tag { color: #34d399; font-weight: 700; font-size: 13px; }
.code-tag { color: #64748b; font-size: 11px; font-family: monospace; }
.desc-tag { color: #e2e8f0; font-size: 13px; font-weight: 500; }

/* ── BOQ table ── */
.boq-table { font-size: 12px; }
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── sidebar ── */
[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
[data-testid="stSidebar"] * { color: #e2e8f0; }

/* ── inputs ── */
[data-testid="stNumberInput"] input, [data-testid="stTextInput"] input {
    background: #1e293b; color: #e2e8f0; border: 1px solid #334155; border-radius: 6px;
}
[data-testid="stSelectbox"] > div > div {
    background: #1e293b; color: #e2e8f0; border: 1px solid #334155;
}

/* ── expander ── */
[data-testid="stExpander"] {
    background: #0d1424; border: 1px solid #1e293b;
    border-radius: 8px; margin-bottom: 6px;
}

/* ── tabs ── */
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: #1e293b; border-radius: 6px 6px 0 0;
    font-weight: 600; color: #64748b; font-size: 13px;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: #1e40af; color: white;
}

/* ── divider ── */
hr { border-color: #1e293b; }

/* ── boq live banner ── */
.boq-banner {
    background: linear-gradient(90deg, #1d4ed8, #7c3aed);
    border-radius: 10px; padding: 10px 16px; margin-bottom: 12px;
    color: white; font-weight: 700; font-size: 14px;
    display: flex; justify-content: space-between; align-items: center;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# SIDEBAR – Project Info & Settings
# ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 Eze Plumbing BOQ")
    st.caption("Huliot HT Pro + Ultra Silent · Apr 2025")
    st.divider()

    st.markdown("**Project Info**")
    st.session_state.project_name = st.text_input("Project / Site Name", st.session_state.project_name, placeholder="e.g. Tower A - Block 3")
    st.session_state.contractor   = st.text_input("Contractor", st.session_state.contractor, placeholder="Contractor name")
    st.session_state.project_date = st.date_input("Date", value=date.fromisoformat(st.session_state.project_date)).isoformat()

    st.divider()
    st.markdown("**Series Filter**")
    st.session_state.series_filter = st.radio("Show Products", ["Both", "HT Pro", "Ultra Silent"], index=0, horizontal=True)

    st.divider()
    st.markdown("**Pricing Settings**")
    st.session_state.discount = st.number_input("Discount %", min_value=0, max_value=100, value=int(st.session_state.discount), step=1)
    st.session_state.incl_gst = st.checkbox("Add GST", value=st.session_state.incl_gst)
    if st.session_state.incl_gst:
        st.session_state.gst_pct = st.number_input("GST %", min_value=0, max_value=28, value=int(st.session_state.gst_pct), step=1)

    st.divider()

    # Excel Import
    st.markdown("**Import / Export**")
    uploaded = st.file_uploader("📤 Import Excel BOQ", type=["xlsx", "xls"], key="excel_import")
    if uploaded:
        ok, msg = import_from_excel(uploaded)
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

    if st.session_state.boq:
        boq_bytes = to_excel_bytes()
        fname = f"{(st.session_state.project_name or 'Plumbing_BOQ').replace(' ','_')}_{st.session_state.project_date}.xlsx"
        st.download_button("📥 Export Excel BOQ", data=boq_bytes, file_name=fname,
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    st.divider()
    if st.session_state.boq:
        gross, _, net, _, grand, total_qty = boq_totals()
        st.markdown(f"**BOQ Items:** {len(st.session_state.boq)} lines ({total_qty} qty)")
        st.markdown(f"**Net Total:** ₹{round(net):,}")
        if st.session_state.incl_gst:
            st.markdown(f"**Grand Total:** ₹{round(grand):,}")
        if st.button("🗑 Clear BOQ", type="secondary", use_container_width=True):
            st.session_state.boq = {}
            st.rerun()


# ──────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────
col_logo, col_title, col_stats = st.columns([1, 4, 3])
with col_logo:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#2563eb,#7c3aed);color:white;
    font-weight:900;font-size:28px;padding:10px 16px;border-radius:10px;
    text-align:center;letter-spacing:2px;">EZE</div>
    """, unsafe_allow_html=True)
with col_title:
    st.markdown("""
    <div style="padding: 6px 0;">
      <div style="font-size:20px;font-weight:800;color:#f1f5f9;">Plumbing Quantity Sheet</div>
      <div style="font-size:12px;color:#475569;">Huliot Pipes & Fittings · HT Pro + Ultra Silent · April 2025 Price List</div>
    </div>
    """, unsafe_allow_html=True)
with col_stats:
    if st.session_state.boq:
        gross, disc_amt, net, gst_amt, grand, total_qty = boq_totals()
        c1, c2 = st.columns(2)
        c1.metric("BOQ Lines", len(st.session_state.boq))
        c2.metric("Net Total", f"₹{round(net):,}")

st.divider()


# ──────────────────────────────────────────────────────────────────
# MAIN TABS
# ──────────────────────────────────────────────────────────────────
tab_dash, tab_search, tab_boq = st.tabs(["📐 Dashboard", "🔍 Search", f"📋 BOQ  ({len(st.session_state.boq)})"])


# ══════════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD
# ══════════════════════════════════════════════════════════════════
with tab_dash:
    pool = get_pool()

    # ── PIPES SECTION ──────────────────────────────────────────────
    st.markdown('<div class="section-head">⬡ &nbsp; PIPES — Click a DN size to view available lengths</div>', unsafe_allow_html=True)

    # Build pipe DN tiles (available ones only)
    pipes_by_dn = {}
    for p in pool:
        if p["cat"] == "PIPE":
            dn = p["dn"]
            if dn not in pipes_by_dn:
                pipes_by_dn[dn] = []
            pipes_by_dn[dn].append(p)

    available_dns = [d for d in PIPE_DNS if d in pipes_by_dn]
    tile_cols = st.columns(len(available_dns)) if available_dns else []

    for i, dn in enumerate(available_dns):
        with tile_cols[i]:
            items = pipes_by_dn[dn]
            label = f"DN {dn}\n{'▼' if st.session_state.active_pipe_dn == dn else '▶'}\n{len(items)} sizes"
            if st.button(label, key=f"pipe_dn_{dn}", use_container_width=True):
                if st.session_state.active_pipe_dn == dn:
                    st.session_state.active_pipe_dn = None
                else:
                    st.session_state.active_pipe_dn = dn
                    st.session_state.active_fit_cat = None
                st.rerun()

    # Pipe expansion panel
    if st.session_state.active_pipe_dn and st.session_state.active_pipe_dn in pipes_by_dn:
        dn = st.session_state.active_pipe_dn
        items = pipes_by_dn[dn]
        with st.expander(f"DN {dn} PIPES — {len(items)} available sizes", expanded=True):
            n_cols = 3
            rows = [items[i:i+n_cols] for i in range(0, len(items), n_cols)]
            for row in rows:
                cols = st.columns(n_cols)
                for j, prod in enumerate(row):
                    with cols[j]:
                        badge = "ht-badge" if prod["series"] == "HT Pro" else "us-badge"
                        series_short = "HT Pro" if prod["series"] == "HT Pro" else "US"
                        in_boq = prod["code"] in st.session_state.boq
                        qty_badge = f" ×{st.session_state.boq[prod['code']]['qty']}" if in_boq else ""
                        st.markdown(f"""
                        <div class="prod-card">
                          <div>
                            <span class="{badge}">{series_short}</span>
                            <span class="code-tag" style="margin-left:6px;">{prod['code']}</span><br/>
                            <span class="desc-tag">{prod['desc']}</span><br/>
                            <span style="color:#64748b;font-size:11px;">DN {prod['dn']} · {prod['siz']}</span>
                            <span class="price-tag" style="margin-left:8px;">₹{prod['pr']:,}{qty_badge}</span>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"+ Add{qty_badge}", key=f"add_pipe_{prod['code']}", use_container_width=True):
                            add_to_boq(prod)
                            st.rerun()

    st.divider()

    # ── FITTINGS SECTION ───────────────────────────────────────────
    st.markdown('<div class="section-head fit-head">⚙ &nbsp; FITTINGS & ACCESSORIES — Click a category to view items</div>', unsafe_allow_html=True)

    # Build fitting categories (available only)
    fit_by_cat = {}
    for p in pool:
        if p["cat"] != "PIPE":
            cat = p["cat"]
            if cat not in fit_by_cat:
                fit_by_cat[cat] = []
            fit_by_cat[cat].append(p)

    available_cats = [fc for fc in FITTING_CATS if fc["key"] in fit_by_cat]

    # Render fitting tiles in rows of 8
    chunk_size = 8
    for chunk_start in range(0, len(available_cats), chunk_size):
        chunk = available_cats[chunk_start:chunk_start + chunk_size]
        cols = st.columns(len(chunk))
        for i, fc in enumerate(chunk):
            with cols[i]:
                cnt = len(fit_by_cat.get(fc["key"], []))
                is_active = st.session_state.active_fit_cat == fc["key"]
                label = f"{fc['emoji']}\n{fc['label'].split(' ', 1)[1] if ' ' in fc['label'] else fc['label']}\n{'▼' if is_active else '▶'} {cnt}"
                if st.button(label, key=f"fit_cat_{fc['key']}", use_container_width=True):
                    if st.session_state.active_fit_cat == fc["key"]:
                        st.session_state.active_fit_cat = None
                    else:
                        st.session_state.active_fit_cat = fc["key"]
                        st.session_state.active_pipe_dn = None
                    st.rerun()

    # Fitting expansion panel
    if st.session_state.active_fit_cat and st.session_state.active_fit_cat in fit_by_cat:
        cat_key = st.session_state.active_fit_cat
        items = fit_by_cat[cat_key]
        fc_info = next((f for f in FITTING_CATS if f["key"] == cat_key), {"label": cat_key})
        with st.expander(f"{fc_info['label']} — {len(items)} items", expanded=True):
            n_cols = 3
            rows = [items[i:i+n_cols] for i in range(0, len(items), n_cols)]
            for row in rows:
                cols = st.columns(n_cols)
                for j, prod in enumerate(row):
                    with cols[j]:
                        badge = "ht-badge" if prod["series"] == "HT Pro" else "us-badge"
                        series_short = "HT Pro" if prod["series"] == "HT Pro" else "US"
                        in_boq = prod["code"] in st.session_state.boq
                        qty_badge = f" ×{st.session_state.boq[prod['code']]['qty']}" if in_boq else ""
                        st.markdown(f"""
                        <div class="prod-card">
                          <div>
                            <span class="{badge}">{series_short}</span>
                            <span class="code-tag" style="margin-left:6px;">{prod['code']}</span><br/>
                            <span class="desc-tag">{prod['desc']}</span><br/>
                            <span style="color:#64748b;font-size:11px;">DN {prod['dn']}</span>
                            <span class="price-tag" style="margin-left:8px;">₹{prod['pr']:,}{qty_badge}</span>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"+ Add{qty_badge}", key=f"add_fit_{prod['code']}", use_container_width=True):
                            add_to_boq(prod)
                            st.rerun()


# ══════════════════════════════════════════════════════════════════
# TAB 2: SEARCH
# ══════════════════════════════════════════════════════════════════
with tab_search:
    search_q = st.text_input("Search", placeholder="🔍 Search by description, item code, DN size, category...", key="search_input", label_visibility="collapsed")
    if search_q.strip():
        q = search_q.lower()
        results = [p for p in get_pool() if (
            q in p["desc"].lower() or q in p["code"].lower() or
            q in p["dn"].lower() or q in p["cat"].lower()
        )][:50]
        st.caption(f"{len(results)} results for '{search_q}'")
        if results:
            n_cols = 3
            rows = [results[i:i+n_cols] for i in range(0, len(results), n_cols)]
            for row in rows:
                cols = st.columns(n_cols)
                for j, prod in enumerate(row):
                    with cols[j]:
                        badge = "ht-badge" if prod["series"] == "HT Pro" else "us-badge"
                        series_short = "HT Pro" if prod["series"] == "HT Pro" else "US"
                        in_boq = prod["code"] in st.session_state.boq
                        qty_badge = f" ×{st.session_state.boq[prod['code']]['qty']}" if in_boq else ""
                        st.markdown(f"""
                        <div class="prod-card">
                          <div>
                            <span class="{badge}">{series_short}</span>
                            <span class="code-tag" style="margin-left:6px;">{prod['code']}</span><br/>
                            <span class="desc-tag">{prod['desc']}</span><br/>
                            <span style="color:#64748b;font-size:11px;">DN {prod['dn']} · {prod['cat']}</span>
                            <span class="price-tag" style="margin-left:8px;">₹{prod['pr']:,}{qty_badge}</span>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"+ Add{qty_badge}", key=f"add_srch_{prod['code']}", use_container_width=True):
                            add_to_boq(prod)
                            st.rerun()
        else:
            st.info("No items found. Try different keywords.")
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#334155;">
          <div style="font-size:48px;margin-bottom:12px;">🔍</div>
          <div style="font-size:17px;font-weight:600;color:#475569;">Type to search all 250+ products</div>
          <div style="font-size:13px;margin-top:8px;">Search by name · item code · DN size · category</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 3: BOQ
# ══════════════════════════════════════════════════════════════════
with tab_boq:
    if not st.session_state.boq:
        st.markdown("""
        <div style="text-align:center;padding:80px 20px;color:#334155;">
          <div style="font-size:48px;margin-bottom:12px;">📋</div>
          <div style="font-size:17px;font-weight:600;color:#475569;">BOQ is empty</div>
          <div style="font-size:13px;margin-top:8px;">Go to Dashboard or Search tab to add items</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        gross, disc_amt, net, gst_amt, grand, total_qty = boq_totals()

        # Summary metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Lines",  len(st.session_state.boq))
        c2.metric("Total Qty",    total_qty)
        c3.metric("Gross Total",  f"₹{round(gross):,}")
        c4.metric("Net Total",    f"₹{round(net):,}")

        st.divider()

        # Editable BOQ table
        st.markdown("**Bill of Quantities — Edit quantities below**")

        items = list(st.session_state.boq.values())
        for idx, item in enumerate(items):
            with st.container():
                c_sr, c_desc, c_dn, c_size, c_up, c_qty, c_amt, c_del = st.columns([0.4, 3.5, 0.8, 1, 1, 0.8, 1.2, 0.5])
                with c_sr:
                    st.markdown(f"<div style='color:#475569;font-size:12px;padding-top:8px;'>{idx+1}</div>", unsafe_allow_html=True)
                with c_desc:
                    badge = "ht-badge" if item["series"] == "HT Pro" else "us-badge"
                    sname = "HT" if item["series"] == "HT Pro" else "US"
                    st.markdown(f"""
                    <div style="padding-top:4px;">
                      <span class="{badge}">{sname}</span>
                      <span style="color:#64748b;font-size:11px;margin-left:6px;font-family:monospace;">{item['code']}</span><br/>
                      <span style="font-size:13px;color:#e2e8f0;">{item['desc']}</span>
                    </div>""", unsafe_allow_html=True)
                with c_dn:
                    st.markdown(f"<div style='padding-top:8px;font-size:12px;color:#94a3b8;'>DN {item['dn']}</div>", unsafe_allow_html=True)
                with c_size:
                    siz_disp = item['siz'] if item['siz'] != '-' else '—'
                    st.markdown(f"<div style='padding-top:8px;font-size:12px;color:#64748b;'>{siz_disp}</div>", unsafe_allow_html=True)
                with c_up:
                    st.markdown(f"<div style='padding-top:8px;font-size:12px;color:#94a3b8;'>₹{item['pr']:,}</div>", unsafe_allow_html=True)
                with c_qty:
                    new_qty = st.number_input("", min_value=0, max_value=9999, value=item["qty"],
                                              key=f"qty_{item['code']}", label_visibility="collapsed")
                    if new_qty != item["qty"]:
                        if new_qty == 0:
                            del st.session_state.boq[item["code"]]
                        else:
                            st.session_state.boq[item["code"]]["qty"] = new_qty
                        st.rerun()
                with c_amt:
                    st.markdown(f"<div style='padding-top:8px;font-size:14px;font-weight:700;color:#34d399;text-align:right;'>₹{item['pr']*item['qty']:,}</div>", unsafe_allow_html=True)
                with c_del:
                    if st.button("✕", key=f"del_{item['code']}", use_container_width=True):
                        del st.session_state.boq[item["code"]]
                        st.rerun()
            if idx < len(items) - 1:
                st.markdown("<hr style='margin:2px 0;border-color:#1e293b;'>", unsafe_allow_html=True)

        st.divider()

        # Totals
        col_empty, col_totals = st.columns([2, 1])
        with col_totals:
            st.markdown("""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:20px 24px;">
            """, unsafe_allow_html=True)
            st.markdown(f"**BOQ Summary**")
            st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:8px;'><span style='color:#94a3b8;'>Gross Total ({total_qty} qty)</span><span style='color:#e2e8f0;font-weight:700;'>₹{round(gross):,}</span></div>", unsafe_allow_html=True)

            if st.session_state.discount > 0:
                st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:8px;'><span style='color:#94a3b8;'>Discount @ {st.session_state.discount}%</span><span style='color:#ef4444;font-weight:700;'>-₹{round(disc_amt):,}</span></div>", unsafe_allow_html=True)

            st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:8px;border-top:1px solid #1e293b;padding-top:10px;'><span style='color:#94a3b8;font-weight:700;'>Net Total (Ex-GST)</span><span style='color:#34d399;font-weight:800;font-size:17px;'>₹{round(net):,}</span></div>", unsafe_allow_html=True)

            if st.session_state.incl_gst:
                st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:8px;'><span style='color:#94a3b8;'>GST @ {st.session_state.gst_pct}%</span><span style='color:#94a3b8;'>+₹{round(gst_amt):,}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='display:flex;justify-content:space-between;border-top:1px solid #334155;padding-top:10px;'><span style='color:#e2e8f0;font-weight:800;font-size:15px;'>GRAND TOTAL</span><span style='color:#f97316;font-weight:900;font-size:20px;'>₹{round(grand):,}</span></div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            st.caption("* Prices are List Price ex-factory/depot. Actual price subject to trade discount.")

            # Export button in BOQ tab too
            boq_bytes = to_excel_bytes()
            fname = f"{(st.session_state.project_name or 'Plumbing_BOQ').replace(' ','_')}_{st.session_state.project_date}.xlsx"
            st.download_button(
                "📥 Download Excel BOQ",
                data=boq_bytes, file_name=fname,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True, type="primary"
            )
