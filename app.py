import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(page_title="Eze Plumbing BOQ", page_icon="🔧",
                   layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════════════════════
#  PIPE DATA  — Huliot APRIL 2026 Price List (verified from PDF)
#  Format per entry: (item_code, DN, price)
# ══════════════════════════════════════════════════════════════════════════════

# ── HT PRO S/S ───────────────────────────────────────────────────────────────
HT_SS = {
    "3000mm": [("54040300-i","40",567),("54050300-i","50",739),("54075300-i","75",1304),
               ("540110300-i","110",1751),("540125300-i","125",3400),("540160300-i","160",4116),
               ("540200300-i","200",8303)],
    "2000mm": [("54040200-i","40",385),("54050200-i","50",503),("54075200-i","75",882),
               ("540110200-i","110",1421),("540125200-i","125",2307),("540160200-i","160",2796)],
    "1500mm": [("54040150-i","40",294),("54050150-i","50",384),("54075150-i","75",672),
               ("540110150-i","110",1085),("540125150-i","125",1759),("540160150-i","160",2134)],
    "1000mm": [("54040100-i","40",204),("54050100-i","50",266),("54075100-i","75",462),
               ("540110100-i","110",747),("540125100-i","125",1212),("540160100-i","160",1474)],
    "500mm":  [("54040050-i","40",113),("54050050-i","50",147),("54075050-i","75",252),
               ("540110050-i","110",411),("540125050-i","125",664),("540160050-i","160",812)],
    "250mm":  [("5404000025-i","40",77),("5405000025-i","50",88),("5407500025-i","75",147),
               ("5401100025-i","110",243),("5401200025-i","125",392),("5401600025-i","160",483)],
}

# ── HT PRO D/S ───────────────────────────────────────────────────────────────
HT_DS = {
    "3000mm": [("5404040300-i","40",588),("5405050300-i","50",768),("5407575300-i","75",1344),
               ("5401111300-i","110",2063),("5401212300-i","125",3518),("5401616300-i","160",4268)],
    "2000mm": [("5404040200-i","40",406),("5405050200-i","50",531),("5407575200-i","75",924),
               ("5401111200-i","110",1494),("5401212200-i","125",2423),("5401616200-i","160",2946)],
    "1500mm": [("5404040150-i","40",315),("5405050150-i","50",413),("5407575150-i","75",712),
               ("5401111150-i","110",1157),("5401212150-i","125",1876),("5401616150-i","160",2286)],
    "1000mm": [("5404040100-i","40",224),("5405050100-i","50",293),("5407575100-i","75",502),
               ("5401111100-i","110",821),("5401212100-i","125",1328),("5401616100-i","160",1624)],
    "500mm":  [("5404040050-i","40",134),("540505050-i","50",175),("5407575050-i","75",292),
               ("5401111050-i","110",484),("5401212050-i","125",782),("5401616050-i","160",964)],
}

# ── ULTRA SILENT S/S ─────────────────────────────────────────────────────────
# Note: DN63 and DN90 removed from 2026 list
US_SS = {
    "3000mm": [("5753200300-i","32",948),("5754000300-i","40",1027),("5755000300-i","50",1313),
               ("5757500300-i","75",2521),("5751100300-i","110",2953),("5751200300-i","125",4165),
               ("5751600300-i","160",6060),("5752000300-i","200",8520)],
    "2000mm": [("5754000200-i","40",697),("5755000200-i","50",890),("5757500200-i","75",1705),
               ("5751100200-i","110",2300),("5751200200-i","125",2821),("5751600200-i","160",4472),
               ("5752000200-i","200",5718)],
    "1500mm": [("5754000150-i","40",531),("5755000150-i","50",680),("5757500150-i","75",1297),
               ("5751100150-i","110",1751),("5751200150-i","125",2390),("5751600150-i","160",3407),
               ("5752000150-i","200",4322)],
    "1000mm": [("5754000100-i","40",366),("5755000100-i","50",468),("5757500100-i","75",890),
               ("5751100100-i","110",1201),("5751200100-i","125",1478),("5751600100-i","160",2340),
               ("5752000100-i","200",2926)],
    "500mm":  [("5754000050-i","40",200),("5755000050-i","50",257),("5757500050-i","75",483),
               ("5751100050-i","110",650),("5751200050-i","125",806),("5751600050-i","160",1274)],
    "250mm":  [("5754000025-i","40",117),("5755000025-i","50",152),("5757500025-i","75",278),
               ("5751100025-i","110",376),("5751200025-i","125",470),("5751600025-i","160",741)],
}

# ── ULTRA SILENT D/S ─────────────────────────────────────────────────────────
# Note: 2026 has proper D/S codes for 500mm (5754040050-i etc.)
US_DS = {
    "3000mm": [("5754040300-i","40",1061),("5755050300-i","50",1358),("5757575300-i","75",2593),
               ("5751111300-i","110",3110),("5751212300-i","125",4300),("5751616300-i","160",6812),
               ("5752020300-i","200",8653)],
    "2000mm": [("5754040200-i","40",730),("5755050200-i","50",935),("5757575200-i","75",1779),
               ("5751111200-i","110",2401),("5751212200-i","125",2957),("5751616200-i","160",4680),
               ("5752020200-i","200",5851)],
    "1500mm": [("5754040150-i","40",564),("5755050150-i","50",724),("5757575150-i","75",1371),
               ("5751111150-i","110",1850),("5751212150-i","125",2470),("5751616150-i","160",3614),
               ("5752020150-i","200",4455)],
    "1000mm": [("5754040100-i","40",400),("5755050100-i","50",514),("5757575100-i","75",964),
               ("5751111100-i","110",1301),("5751212100-i","125",1613),("5751616100-i","160",2547),
               ("5752020100-i","200",3059)],
    "500mm":  [("5754040050-i","40",234),("5755050050-i","50",302),("5757575050-i","75",556),
               ("5751111050-i","110",751),("5751212050-i","125",947),("5751616050-i","160",1482)],
}


def _build_pipes(table, sock_type, series, prefix):
    rows = []
    for length, items in table.items():
        for code, dn, pr in items:
            rows.append({"code":code,"dn":dn,"pr":pr,"cat":"PIPE",
                         "desc":f"{prefix} {sock_type} PIPE",
                         "siz":f"{length} {sock_type}","series":series})
    return rows


# ══════════════════════════════════════════════════════════════════════════════
#  FITTINGS — April 2026
# ══════════════════════════════════════════════════════════════════════════════
def _f(code, desc, cat, dn, pr, siz="-"):
    return {"code":code,"desc":desc,"cat":cat,"dn":dn,"pr":pr,"siz":siz}

HT_FITTINGS = [
    # BENDS
    _f("40040150","HT PRO BEND 15 DEG","BEND","110",234),
    _f("40040350","HT PRO BEND 30 DEG","BEND","110",239),
    _f("40010460-i","HT PRO BEND 45 DEG","BEND","40",66),
    _f("40020460-i","HT PRO BEND 45 DEG","BEND","50",82),
    _f("40030460-i","HT PRO BEND 45 DEG","BEND","75",128),
    _f("40040460-i","HT PRO BEND 45 DEG","BEND","110",186),
    _f("40050460","HT PRO BEND 45 DEG","BEND","125",768),
    _f("40060460","HT PRO BEND 45 DEG","BEND","160",1013),
    _f("40010860-i","HT PRO BEND 87.5 DEG","BEND","40",72),
    _f("40020860-i","HT PRO BEND 87.5 DEG","BEND","50",77),
    _f("40030860","HT PRO BEND 87.5 DEG","BEND","75",155),
    _f("40040860-i","HT PRO BEND 87.5 DEG","BEND","110",270),
    _f("40050860","HT PRO BEND 87.5 DEG","BEND","125",1058),
    _f("40060860","HT PRO BEND 87.5 DEG","BEND","160",722),
    # DOOR BENDS
    _f("40020467","HT PRO DOOR BEND 45 DEG","DOOR BEND","50",149),
    _f("40040467","HT PRO DOOR BEND 45 DEG","DOOR BEND","110",456),
    _f("40040468","HT PRO DOOR BEND 45 DEG (R)","DOOR BEND","110",386),
    _f("40040469","HT PRO DOOR BEND 45 DEG (L)","DOOR BEND","110",382),
    _f("40060457","HT PRO DOOR BEND 45 DEG","DOOR BEND","160",1751),
    _f("40060458","HT PRO DOOR BEND 45 DEG (R)","DOOR BEND","160",1504),
    _f("40060459","HT PRO DOOR BEND 45 DEG (L)","DOOR BEND","160",1626),
    _f("40020867-i","HT PRO DOOR BEND 87.5 DEG","DOOR BEND","50",221),
    _f("40030867","HT PRO DOOR BEND 87.5 DEG","DOOR BEND","75",209),
    _f("40040867-i","HT PRO DOOR BEND 87.5 DEG","DOOR BEND","110",517),
    _f("40060857","HT PRO DOOR BEND 87.5 DEG","DOOR BEND","160",2429),
    _f("40040868-i","HT PRO DOOR BEND 87.5 (R)","DOOR BEND","110",553),
    _f("40040869","HT PRO DOOR BEND 87.5 (L)","DOOR BEND","110",565),
    _f("40060858","HT PRO DOOR BEND 87.5 (R)","DOOR BEND","160",1907),
    _f("40060859","HT PRO DOOR BEND 87.5 (L)","DOOR BEND","160",1927),
    # WYE
    _f("40611440","HT PRO SINGLE Y 40x40","WYE","40x40",96),
    _f("40622460","HT PRO SINGLE Y 50x50","WYE","50x50",139),
    _f("40633460-i","HT PRO SINGLE Y 75x75","WYE","75x75",262),
    _f("40644460-i","HT PRO SINGLE Y 110x110","WYE","110x110",575),
    _f("40655460","HT PRO SINGLE Y 125x125","WYE","125x125",4483),
    _f("40666450","HT PRO SINGLE Y 160x160","WYE","160x160",1942),
    _f("40621440","HT PRO REDUCING Y 50x40","WYE","50x40",143),
    _f("40632460","HT PRO REDUCING Y 75x50","WYE","75x50",350),
    _f("40642460","HT PRO REDUCING Y 110x50","WYE","110x50",361),
    _f("40643460","HT PRO REDUCING Y 110x75","WYE","110x75",578),
    _f("40654460","HT PRO REDUCING Y 125x110","WYE","125x110",3022),
    _f("40664450","HT PRO REDUCING Y 160x110","WYE","160x110",2267),
    _f("41042450","HT PRO DOUBLE Y 110x50x50","WYE","110x50x50",1560),
    _f("41044450","HT PRO DOUBLE Y 110x110x110","WYE","110x110x110",1463),
    _f("41062450","HT PRO RED. DOUBLE Y 160x50x50","WYE","160x50x50",1225),
    _f("41044457","HT PRO DOUBLE Y DOOR 110x110x110","WYE","110x110x110",3106),
    # TEE
    _f("40611860","HT PRO SINGLE TEE 40x40","TEE","40x40",110),
    _f("40622860","HT PRO SINGLE TEE 50x50","TEE","50x50",121),
    _f("40633860-i","HT PRO SINGLE TEE 75x75","TEE","75x75",197),
    _f("40655860","HT PRO SINGLE TEE 125x125","TEE","125x125",607),
    _f("40666860","HT PRO SINGLE TEE 160x160","TEE","160x160",947),
    _f("40621860","HT PRO REDUCING TEE 50x40","TEE","50x40",166),
    _f("40632860","HT PRO REDUCING TEE 75x50","TEE","75x50",185),
    _f("40642860","HT PRO REDUCING TEE (S) 110x50","TEE","110x50",392),
    _f("40652860","HT PRO REDUCING TEE 125x50","TEE","125x50",614),
    _f("40662860","HT PRO REDUCING TEE 160x50","TEE","160x50",1093),
    _f("40664860","HT PRO REDUCING TEE 160x110","TEE","160x110",877),
    # SWEPT TEE
    _f("40733860-i","HT PRO SWEPT TEE 75x75","SWEPT TEE","75x75",260),
    _f("40742860-i","HT PRO SWEPT TEE 110x50","SWEPT TEE","110x50",436),
    _f("40743860-i","HT PRO SWEPT TEE 110x75","SWEPT TEE","110x75",550),
    _f("40744860-i","HT PRO SWEPT TEE 110x110","SWEPT TEE","110x110",510),
    _f("40754860","HT PRO SWEPT TEE 125x110","SWEPT TEE","125x110",1080),
    _f("14040764860-i","HT PRO SWEPT TEE 160x110","SWEPT TEE","160x110",2086),
    _f("41044860","HT PRO DOUBLE SWEPT TEE 110x110x110","SWEPT TEE","110x110x110",2023),
    _f("41064850","HT PRO DOUBLE BRANCH 160x110x110","SWEPT TEE","160x110x110",2754),
    # DOOR SWEPT TEE (2026 adds 125x110)
    _f("40733867-i","HT PRO DOOR SWEPT TEE 75x75","SWEPT TEE","75x75",460),
    _f("40742867-i","HT PRO DOOR SWEPT TEE 110x50","SWEPT TEE","110x50",616),
    _f("40743867-i","HT PRO DOOR SWEPT TEE 110x75","SWEPT TEE","110x75",732),
    _f("40744867-i","HT PRO DOOR SWEPT TEE 110x110","SWEPT TEE","110x110",754),
    _f("40754867-HM","HT PRO DOOR SWEPT TEE 125x110","SWEPT TEE","125x110",2016),
    _f("40664857-i","HT PRO DOOR SWEPT TEE 160x110","SWEPT TEE","160x110",2766),
    _f("41044857-HM","HT PRO DOUBLE DOOR SWEPT TEE 110x110x110","SWEPT TEE","110x110x110",2232),
    # CORNER BRANCH
    _f("41244850","HT PRO CORNER BRANCH 110x110x110","CORNER BRANCH","110x110x110",1346),
    _f("4041254850","HT PRO CORNER BRANCH 125x110x110","CORNER BRANCH","125x110x110",1968),
    _f("41264850-i","HT PRO RED. CORNER BRANCH 160x110x110","CORNER BRANCH","160x110x110",2382),
    # TRAP
    _f("49540750 G-i","HT PRO P TRAP 50mm W.S.","TRAP","110x110",1132),
    _f("41840051-i","HT PRO S TRAP SIPHON TYPE","TRAP","110x110",2262),
    _f("69111750 G-i","HT PRO NAHANI TRAP","TRAP","110x75",649),
    # MFT
    _f("60117051","HT PRO MULTI FLOOR TRAP 7\"","MFT","110x75x50",1256),
    _f("14048111060 G-i","HT PRO MFT WITH SOCKET","MFT","110x75x50",1680),
    # HEIGHT RISER
    _f("69201551 G-i","HT PRO HEIGHT RISER L150 (MFT)","HEIGHT RISER","110",497),
    _f("69203551 G-i","HT PRO HEIGHT RISER L350 (MFT)","HEIGHT RISER","110",737),
    _f("60203651-i","HT PRO HEIGHT RISER THREAD LOCK","HEIGHT RISER","110",109),
    _f("41242850-i","HT. RISER 2 INLET 90 DEG","HEIGHT RISER","110x50x50",1061),
    _f("41042860","HT. RISER 2 INLET 180 DEG","HEIGHT RISER","110x50x50",1265),
    _f("4102042860","HT. RISER WITH 3 INLET","HEIGHT RISER","110x50x50x50",1380),
    _f("4041043280","HT. RISER 50 & 75MM INLET","HEIGHT RISER","110x75x50",1038),
    # H.A.F.F STACK
    _f("4049911100 G-i","HT PRO H.A.F.F STACK FOR SINGLE STACK","SPECIAL","110x110x75",6600),
    # INSPECTION
    _f("49130060-i","HT PRO CLEANING PIPE","INSPECTION","75",460),
    _f("49140060-i","HT PRO CLEANING PIPE","INSPECTION","110",566),
    _f("49150060","HT PRO CLEANING PIPE","INSPECTION","125",1249),
    _f("49160060","HT PRO CLEANING PIPE","INSPECTION","160",1199),
    # COUPLER
    _f("41710055-i","HT PRO COUPLER DN40","COUPLER","40",73),
    _f("41720055-i","HT PRO COUPLER DN50","COUPLER","50",85),
    _f("41730050-i","HT PRO COUPLER DN75","COUPLER","75",115),
    _f("41740055-i","HT PRO COUPLER DN110","COUPLER","110",210),
    _f("41750065","HT PRO COUPLER DN125","COUPLER","125",494),
    _f("41760055","HT PRO COUPLER DN160","COUPLER","160",1054),
    # SLEEVE
    _f("41720053","HT PRO SLEEVE DN50","SLEEVE","50",115),
    _f("41730053","HT PRO SLEEVE DN75","SLEEVE","75",128),
    _f("41740053","HT PRO SLEEVE DN110","SLEEVE","110",215),
    # REDUCER
    _f("42121060","HT PRO ECCENTRIC REDUCER 50x40","REDUCER","50x40",66),
    _f("42132050","HT PRO ECCENTRIC REDUCER 75x50","REDUCER","75x50",83),
    _f("42142050","HT PRO ECCENTRIC REDUCER 110x50","REDUCER","110x50",182),
    _f("42143050-i","HT PRO ECCENTRIC REDUCER 110x75","REDUCER","110x75",215),
    _f("42154060","HT PRO ECCENTRIC REDUCER 125x110","REDUCER","125x110",421),
    _f("42164050","HT PRO ECCENTRIC REDUCER 160x110","REDUCER","160x110",653),
    _f("42134050-i","HT PRO REVERSE REDUCER 110x75","REDUCER","110x75",510),  # NEW 2026
    _f("P0500000000040K","HT PRO CONCENTRIC REDUCER 50x40","REDUCER","50x40",192),
    _f("P07500000050K","HT PRO CONCENTRIC REDUCER 75x50","REDUCER","75x50",253),
    _f("P1100000000050V","HT PRO CONCENTRIC REDUCER 110x50","REDUCER","110x50",328),
    _f("P1100000000075V","HT PRO CONCENTRIC REDUCER 110x75","REDUCER","110x75",401),
    # END CAP
    _f("41610040","HT PRO END CAP DN40","END CAP","40",35),
    _f("41620050-i","HT PRO END CAP DN50","END CAP","50",66),
    _f("41630050-i","HT PRO END CAP DN75","END CAP","75",70),
    _f("41640050-i","HT PRO END CAP DN110","END CAP","110",115),
    _f("41650060","HT PRO END CAP DN125","END CAP","125",251),
    _f("41660060","HT PRO END CAP DN160","END CAP","160",344),
    # VENT COWL
    _f("4042320040","HT PRO VENT COWL DN50","VENT COWL","50",239),
    _f("4042330040","HT PRO VENT COWL DN75","VENT COWL","75",185),
    _f("4042340060","HT PRO VENT COWL DN110","VENT COWL","110",194),
    _f("4042360040","HT PRO VENT COWL DN160","VENT COWL","160",413),
    # BOSS CONNECTOR — NEW IN 2026
    _f("5401106650-i","HT PRO BOSS PIPE SINGLE INLET 110x50","BOSS CONN","110x50",1004,"L660mm"),
    _f("540110502-i","HT PRO BOSS PIPE DOUBLE BRANCH 110x50x50","BOSS CONN","110x50x50",1404,"L660mm"),
    _f("5401105102-i","HT PRO BOSS PIPE CORNER BRANCH 110x50x50","BOSS CONN","110x50x50",1404,"L660mm"),
    _f("540110503-i","HT PRO BOSS PIPE TRIPLE BRANCH 110x50x50x50","BOSS CONN","110x50x50x50",1604,"L660mm"),
    # CLAMPS
    _f("48100040-S","HT PRO CLAMP DN40","CLAMP","40",105),
    _f("48100050-S","HT PRO CLAMP DN50","CLAMP","50",115),
    _f("48100075-S","HT PRO CLAMP DN75","CLAMP","75",145),
    _f("48100011-S","HT PRO CLAMP DN110","CLAMP","110",175),
    _f("48100012-S","HT PRO CLAMP DN125","CLAMP","125",205),
    _f("48100016-S","HT PRO CLAMP DN160","CLAMP","160",250),
    _f("48100020-S","HT PRO CLAMP DN200","CLAMP","200",295),
    # SHOWER CHANNEL
    _f("60150331","AQUASLIM S.STEEL L/330mm","SHOWER CHANNEL","-",1288,"330mm"),
    _f("60150339","AQUASLIM FULL S.STEEL 330 TILES","SHOWER CHANNEL","-",1333,"330mm"),
    _f("60150701","AQUASLIM S.STEEL L/700mm","SHOWER CHANNEL","-",1790,"700mm"),
    _f("60150709","AQUASLIM FULL S.STEEL 700 TILES","SHOWER CHANNEL","-",1939,"700mm"),
    _f("60200260","EXTENSION FOR SQUARE GRATING","SHOWER CHANNEL","-",82),
    _f("60200263","EXTENSION FOR SQUARE GRATING","SHOWER CHANNEL","-",78),
    # WC CONNECTOR
    _f("41540020","STRAIGHT WC CONNECTOR","WC CONN","CONN",1558),
    _f("41540027","DOOR STRAIGHT WC CONNECTOR INSP.","WC CONN","INSP",1776),
    _f("41542866","WC BEND WITH DOOR INSPECTION","WC CONN","INSP",1559),
    _f("41540615","FLANGE FOR WC BEND - WHITE","WC CONN","FLANGE",66),
    # ACCESSORIES
    _f("47700012","LUBRICANT TIN 250ML","ACCESSORIES","-",198),
]

US_FITTINGS = [
    # BENDS 15 DEG
    _f("7070000170","US BEND 15 DEG","BEND","32",61),
    _f("7070010170","US BEND 15 DEG","BEND","40",82),
    _f("7070020170","US BEND 15 DEG","BEND","50",102),
    _f("7070030170","US BEND 15 DEG","BEND","75",184),
    _f("7070040170","US BEND 15 DEG","BEND","110",698),
    _f("7070050170","US BEND 15 DEG","BEND","125",694),
    _f("7070060170","US BEND 15 DEG","BEND","160",1357),
    # BENDS 30 DEG
    _f("7070000370","US BEND 30 DEG","BEND","32",82),
    _f("7070010370","US BEND 30 DEG","BEND","40",102),
    _f("7070020370","US BEND 30 DEG","BEND","50",102),
    _f("7070030370","US BEND 30 DEG","BEND","75",205),
    _f("7070040370","US BEND 30 DEG","BEND","110",727),
    _f("7070050370","US BEND 30 DEG","BEND","125",838),
    _f("7070060370","US BEND 30 DEG","BEND","160",1330),
    # BENDS 45 DEG
    _f("7070000470","US BEND 45 DEG","BEND","32",61),
    _f("7070010470","US BEND 45 DEG","BEND","40",82),
    _f("7070020470","US BEND 45 DEG","BEND","50",122),
    _f("7070030470-i","US BEND 45 DEG","BEND","75",205),
    _f("7070040470-i","US BEND 45 DEG","BEND","110",641),
    _f("7070050470","US BEND 45 DEG","BEND","125",899),
    _f("7070060470","US BEND 45 DEG","BEND","160",1202),
    _f("7070080470","US BEND 45 DEG","BEND","200",3493),
    # BENDS 67.5 DEG
    _f("7070000670","US BEND 67.5 DEG","BEND","32",61),
    _f("7070010670","US BEND 67.5 DEG","BEND","40",61),
    _f("7070020670","US BEND 67.5 DEG","BEND","50",82),
    _f("7070030670","US BEND 67.5 DEG","BEND","75",122),
    _f("7070040670","US BEND 67.5 DEG","BEND","110",632),
    _f("7070050670","US BEND 67.5 DEG","BEND","125",643),
    # BENDS 87.5 DEG
    _f("7070000870","US BEND 87.5 DEG","BEND","32",61),
    _f("7070010870","US BEND 87.5 DEG","BEND","40",102),
    _f("7070020870-i","US BEND 87.5 DEG","BEND","50",143),
    _f("7070030870","US BEND 87.5 DEG","BEND","75",224),
    _f("7070040870","US BEND 87.5 DEG","BEND","110",697),
    _f("7070050870","US BEND 87.5 DEG","BEND","125",1062),
    _f("7070060870","US BEND 87.5 DEG","BEND","160",2122),
    _f("7070040877-i","US DOOR BEND 87.5 DEG","BEND","110",1054),  # NEW 2026
    # WYE (90x90, 90x50, 110x90 removed from 2026)
    _f("7070600470","US WYE 32x32","WYE","32x32",194),
    _f("7070611470","US WYE 40x40","WYE","40x40",274),
    _f("7070621470","US WYE 50x40","WYE","50x40",352),
    _f("7070622470","US WYE 50x50","WYE","50x50",390),
    _f("7070632470","US WYE 75x50","WYE","75x50",523),
    _f("7070633470","US WYE 75x75","WYE","75x75",698),
    _f("7070642470","US WYE 110x50","WYE","110x50",640),
    _f("7070643470-i","US WYE 110x75","WYE","110x75",959),
    _f("7070644470-i","US WYE 110x110","WYE","110x110",1183),
    _f("7070654470","US WYE 125x110","WYE","125x110",1489),
    _f("7070655470","US WYE 125x125","WYE","125x125",1754),
    _f("7070664470","US WYE 160x110","WYE","160x110",2672),
    _f("7070666470","US WYE 160x160","WYE","160x160",3653),
    _f("7070686470","US WYE 200x160","WYE","200x160",6776),
    _f("7070688470","US WYE 200x200","WYE","200x200",7529),
    # TEE (90x50 removed 2026)
    _f("7070611870","US TEE 40x40","TEE","40x40",312),
    _f("7070621870","US TEE 50x40","TEE","50x40",352),
    _f("7070622870","US TEE 50x50","TEE","50x50",352),
    _f("7070632870","US TEE 75x50","TEE","75x50",553),
    _f("7070633870","US TEE 75x75","TEE","75x75",781),
    _f("7070642870","US TEE 110x50","TEE","110x50",898),
    _f("7070666870","US TEE 160x160","TEE","160x160",3122),
    # SWEPT TEE (2026 adds door variants for 125x110 & 160x110)
    _f("7070744870","US SWEPT TEE 110x110","SWEPT TEE","110x110",1081),
    _f("7070743870","US SWEPT TEE 110x75","SWEPT TEE","110x75",938),
    _f("7070754870","US SWEPT TEE 125x110","SWEPT TEE","125x110",1062),
    _f("7070764870","US SWEPT TEE 160x110","SWEPT TEE","160x110",2366),
    _f("7070744877","US DOOR SWEPT TEE 110x110","SWEPT TEE","110x110",1342),
    _f("7070754877-i","US DOOR SWEPT TEE 125x110","SWEPT TEE","125x110",1740),  # NEW 2026
    _f("7070764877-i","US DOOR SWEPT TEE 160x110","SWEPT TEE","160x110",2752),  # NEW 2026
    _f("7071044870","US DOUBLE SWEPT TEE 110x110x110","SWEPT TEE","110x110x110",2970),
    # CORNER BRANCH
    _f("7071244870","US CORNER BRANCH 110x110x110","CORNER BRANCH","110x110x110",1285),
    _f("7071254870","US CORNER BRANCH 125x110x110","CORNER BRANCH","125x110x110",1489),
    # DOUBLE BRANCH
    _f("7071042670","US DOUBLE BRANCH 67.5 DEG 110x50x50","DOUBLE BRANCH","110x50x50",1105),
    _f("7071044670","US DOUBLE BRANCH 67.5 DEG 110x110x110","DOUBLE BRANCH","110x110x110",1518),
    # TRAP
    _f("49540750 B-i","US P TRAP 50mm W.S.","TRAP","110x110",1435),
    _f("7071840070-i","US S TRAP 110mm","TRAP","110x110",2870),
    _f("69111750 B-i","US NAHANI TRAP","TRAP","110x75",781),
    # MFT
    _f("60117060","US MULTI FLOOR TRAP W/O RING","MFT","110x75x50",1496),
    _f("S11050505075-i","US MULTI FLOOR TRAP WITH RING","MFT","110x75x50",1778),
    _f("17078111070-B","US MULTI FLOOR TRAP WITH SOCKET","MFT","110x75x50",1835),
    # SMARTLOCK
    _f("70114500","SMARTLOCK TRAP 140/50 SINGLE DISCHARGE","SMARTLOCK","98.3x50",1243),
    _f("70124599","SMARTLOCK TRAP 245/50 SINGLE DISCHARGE","SMARTLOCK","50x40",1499),
    _f("70114590","SMARTLOCK TRAP 140/40/50 MULTI DISCHARGE","SMARTLOCK","50x40",1820),
    _f("70124590","SMARTLOCK TRAP 245/40/50 MULTI DISCHARGE","SMARTLOCK","98.3x50",2047),
    _f("70140760","COLLECTOR 70/40 SINGLE DISCHARGE W/O TRAP","SMARTLOCK","98.4x40",760),
    # HEIGHT RISER MFT
    _f("69201551 B-i","US HEIGHT RISER L150 (MFT)","HEIGHT RISER","110",650),
    _f("69203551 B-i","US HEIGHT RISER L350 (MFT)","HEIGHT RISER","110",977),
    _f("60203651-i","HEIGHT RISER FOR SMART LOCK TRAP","HEIGHT RISER","110",109),
    # HEIGHT RISER P TRAP
    _f("7071042877-i","US DOUBLE BRANCH 180 DEG 110x50x50","HEIGHT RISER","110x50x50",1289),
    _f("7071242877-i","US CORNER BRANCH 90 DEG 110x50x50","HEIGHT RISER","110x50x50",1459),
    _f("70712","US HOPPER WITH 3 INLET 110x50x50x50","HEIGHT RISER","110x50x50x50",1674),
    _f("70713-i","US HOPPER WITH 3 INLET 110x75x75x75","HEIGHT RISER","110x75x75x75",1958),
    _f("7071043870-i","US DOUBLE BRANCH 180 DEG 110x75x75","HEIGHT RISER","110x75x75",1778),
    _f("7071243870-HM","US CORNER BRANCH 90 DEG 110x75x75","HEIGHT RISER","110x75x75",1778),
    # H.A.F.F STACK
    _f("7079911100 B-i","US H.A.F.F STACK 110x110x75","SPECIAL","110x110x75",9000),
    # INSPECTION
    _f("7079120070","US INSPECTION PIPE DN50","INSPECTION","50",349),
    _f("7079130070","US INSPECTION PIPE DN75","INSPECTION","75",821),
    _f("7079140070","US INSPECTION PIPE DN110","INSPECTION","110",1530),
    _f("7079150070","US INSPECTION PIPE DN125","INSPECTION","125",1775),
    _f("7079160070","US INSPECTION PIPE DN160","INSPECTION","160",1859),
    _f("7079180070","US INSPECTION PIPE DN200","INSPECTION","200",5498),
    # SLEEVE
    _f("7071710070","US SLEEVE DN40","SLEEVE","40",349),
    _f("7071720070","US SLEEVE DN50","SLEEVE","50",821),
    _f("7071730070","US SLEEVE DN75","SLEEVE","75",898),
    _f("7071740070","US SLEEVE DN110","SLEEVE","110",1775),
    _f("7071750070","US SLEEVE DN125","SLEEVE","125",1913),
    _f("7071760070","US SLEEVE DN160","SLEEVE","160",5498),
    # COUPLER
    _f("7071700270","US DOUBLE SOCKET DN32","COUPLER","32",157),
    _f("7071710270","US DOUBLE SOCKET DN40","COUPLER","40",193),
    _f("7071720275","US ONE WAY SOCKET DN50","COUPLER","50",194),
    _f("7071730275-i","US ONE WAY SOCKET DN75","COUPLER","75",352),
    _f("7071740275-i","US ONE WAY SOCKET DN110","COUPLER","110",640),
    _f("7071750275","US ONE WAY SOCKET DN125","COUPLER","125",878),
    _f("7071760275","US ONE WAY SOCKET DN160","COUPLER","160",1717),
    _f("7071780275","US ONE WAY SOCKET DN200","COUPLER","200",2594),
    # REDUCER (90x50, 90x75, 110x90 removed from 2026)
    _f("7072110070","US REDUCER 40x32","REDUCER","40x32",386),
    _f("7072120070","US REDUCER 50x32","REDUCER","50x32",391),
    _f("7072121070","US REDUCER 50x40","REDUCER","50x40",398),
    _f("7072132070","US REDUCER 75x50","REDUCER","75x50",426),
    _f("7072142070","US REDUCER 110x50","REDUCER","110x50",469),
    _f("7072143070","US REDUCER 110x75","REDUCER","110x75",491),
    _f("7072154070","US REDUCER 125x110","REDUCER","125x110",613),
    _f("7072164070","US REDUCER 160x110","REDUCER","160x110",1021),
    _f("7072165070","US REDUCER 160x125","REDUCER","160x125",1163),
    _f("7072186070","US REDUCER 200x160","REDUCER","200x160",2327),
    _f("7072134070-i","US REVERSE REDUCER 110x75","REDUCER","110x75",510),  # NEW 2026
    # END CAP (DN90 removed 2026)
    _f("7071610070","US END CAP DN40","END CAP","40",40),
    _f("7071620070-i","US END CAP DN50","END CAP","50",78),
    _f("7071630070","US END CAP DN75","END CAP","75",157),
    _f("7071640070-i","US END CAP DN110","END CAP","110",352),
    _f("7071650070","US END CAP DN125","END CAP","125",757),
    _f("7071660070","US END CAP DN160","END CAP","160",768),
    _f("7071680070","US END CAP DN200","END CAP","200",1616),
    # LOCK SEAL
    _f("7072330000","US LOCK SEAL DN75","SEAL","75",434),
    _f("7072340000","US LOCK SEAL DN110","SEAL","110",965),
    _f("7072350000","US LOCK SEAL DN125","SEAL","125",1115),
    _f("7072360000","US LOCK SEAL DN160","SEAL","160",1372),
    _f("7072380000","US LOCK SEAL DN200","SEAL","200",6918),
    # END LOCK
    _f("7078004000","US END LOCK DN110","SEAL","110",1518),
    _f("7078005000","US END LOCK DN125","SEAL","125",1663),
    _f("7078006000","US END LOCK DN160","SEAL","160",1702),
    _f("7078008000","US END LOCK DN200","SEAL","200",9194),
    # VENT COWL
    _f("42320040","US VENT CAP DN50","VENT COWL","50",239),
    _f("42330040","US VENT CAP DN75","VENT COWL","75",185),
    _f("42340060","US VENT CAP DN110","VENT COWL","110",194),
    _f("42360040","US VENT CAP DN160","VENT COWL","160",413),
    # CLAMPS
    _f("7890004070-S","US HD SPLIT CLAMP DN40","CLAMP","40",190),
    _f("7890005070-S","US HD SPLIT CLAMP DN50","CLAMP","50",215),
    _f("7890007570-S","US HD SPLIT CLAMP DN75","CLAMP","75",260),
    _f("7890011070-S","US HD SPLIT CLAMP DN110","CLAMP","110",340),
    _f("7890012570-S","US HD SPLIT CLAMP DN125","CLAMP","125",360),
    _f("7890016070-S","US HD SPLIT CLAMP DN160","CLAMP","160",450),
    _f("7890020070-S","US HD SPLIT CLAMP DN200","CLAMP","200",525),
    # CAST IRON
    _f("41740060","DOUBLE SOCKET FOR CAST IRON + SEAL DN110","CAST IRON","110",1019),
    _f("41760051","DOUBLE SOCKET FOR CAST IRON + SEAL DN160","CAST IRON","160",1192),
    # TECHNICAL BEND
    _f("7074010970","USSW TECHNICAL BEND / SIPHON CONNECTOR","TECHNICAL BEND","46",193),
    _f("7074021970","USSW TECHNICAL BEND / SIPHON CONNECTOR","TECHNICAL BEND","50",215),
    _f("7074011970","USSW TECHNICAL BEND / SIPHON CONNECTOR","TECHNICAL BEND","46",193),
    _f("7074022970","USSW TECHNICAL BEND / SIPHON CONNECTOR","TECHNICAL BEND","50",193),
    _f("7074021971","LONG USSW TECHNICAL BEND","TECHNICAL BEND","50",302,"Long"),
    _f("7074011971","LONG USSW TECHNICAL BEND","TECHNICAL BEND","46",302,"Long"),
    # RUBBER GASKET
    _f("T047T000000000","RUBBER GASKET FOR US/USSW/USSWL","ACCESSORIES","46",217),
    _f("T046T000000000","RUBBER GASKET FOR US/USSW/USSWL","ACCESSORIES","46",217),
    _f("T050T000000032","RUBBER GASKET FOR US/USSW/USSWL","ACCESSORIES","50",308),
    _f("T050T000000040","RUBBER GASKET FOR US/USSW/USSWL","ACCESSORIES","50",308),
    # WC CONNECTOR
    _f("41540020-US","STRAIGHT WC CONNECTOR","WC CONN","110",1558),
    _f("41540027-US","STRAIGHT WC CONNECTOR WITH INSPECTION","WC CONN","110",1776),
    _f("41542866-US","WC CONNECTOR BEND WITH INSPECTION","WC CONN","110",1559),
    # ACCESSORIES
    _f("47700012-US","LUBRICANT 250ML","ACCESSORIES","-",198),
]

# ══════════════════════════════════════════════════════════════════════════════
#  BUILD FULL PRODUCT LIST
# ══════════════════════════════════════════════════════════════════════════════
ALL_PRODUCTS = (
    _build_pipes(HT_SS, "S/S", "HT Pro", "HT PRO") +
    _build_pipes(HT_DS, "D/S", "HT Pro", "HT PRO") +
    _build_pipes(US_SS, "S/S", "Ultra Silent", "US") +
    _build_pipes(US_DS, "D/S", "Ultra Silent", "US") +
    [dict(f, series="HT Pro") for f in HT_FITTINGS] +
    [dict(f, series="Ultra Silent") for f in US_FITTINGS]
)

PIPE_DNS = ["32","40","50","63","75","90","110","125","160","200"]

FITTING_CATS = [
    {"key":"BEND","emoji":"🔄","label":"BENDS"},
    {"key":"DOOR BEND","emoji":"🚪","label":"DOOR BENDS"},
    {"key":"WYE","emoji":"⑂","label":"WYE / Y"},
    {"key":"TEE","emoji":"⊤","label":"TEES"},
    {"key":"SWEPT TEE","emoji":"↪","label":"SWEPT TEE"},
    {"key":"CORNER BRANCH","emoji":"↙","label":"CORNER BRANCH"},
    {"key":"DOUBLE BRANCH","emoji":"⑃","label":"DOUBLE BRANCH"},
    {"key":"TRAP","emoji":"∪","label":"TRAPS"},
    {"key":"MFT","emoji":"⊞","label":"MFT"},
    {"key":"SMARTLOCK","emoji":"🔒","label":"SMARTLOCK"},
    {"key":"HEIGHT RISER","emoji":"↕","label":"HEIGHT RISER"},
    {"key":"BOSS CONN","emoji":"🔗","label":"BOSS CONN."},
    {"key":"INSPECTION","emoji":"🔍","label":"INSPECTION"},
    {"key":"COUPLER","emoji":"○","label":"COUPLERS"},
    {"key":"SLEEVE","emoji":"⊃","label":"SLEEVE"},
    {"key":"REDUCER","emoji":"◁","label":"REDUCERS"},
    {"key":"END CAP","emoji":"◼","label":"END CAPS"},
    {"key":"VENT COWL","emoji":"↑","label":"VENT COWL"},
    {"key":"SEAL","emoji":"🔵","label":"SEAL / LOCK"},
    {"key":"CLAMP","emoji":"🗜","label":"CLAMPS"},
    {"key":"WC CONN","emoji":"⊕","label":"WC CONN."},
    {"key":"SHOWER CHANNEL","emoji":"🚿","label":"SHOWER CHANNEL"},
    {"key":"TECHNICAL BEND","emoji":"🔧","label":"TECH BEND"},
    {"key":"CAST IRON","emoji":"⚙","label":"CAST IRON"},
    {"key":"SPECIAL","emoji":"★","label":"SPECIAL"},
    {"key":"ACCESSORIES","emoji":"🔩","label":"ACCESSORIES"},
]

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "boq":{}, "active_pipe_dn":None, "pipe_filter":"Both",
        "active_fit_cat":None, "series_filter":"Both",
        "project_name":"", "contractor":"",
        "project_date":str(date.today()),
        "discount":0, "gst_pct":18, "incl_gst":False,
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def get_pool():
    sf = st.session_state.series_filter
    if sf == "HT Pro":       return [p for p in ALL_PRODUCTS if p["series"]=="HT Pro"]
    if sf == "Ultra Silent": return [p for p in ALL_PRODUCTS if p["series"]=="Ultra Silent"]
    return ALL_PRODUCTS

def add_to_boq(prod):
    c = prod["code"]
    if c in st.session_state.boq: st.session_state.boq[c]["qty"] += 1
    else: st.session_state.boq[c] = dict(prod, qty=1)

def boq_totals():
    items = list(st.session_state.boq.values())
    gross = sum(i["pr"]*i["qty"] for i in items)
    disc  = gross * st.session_state.discount / 100
    net   = gross - disc
    gst   = net * st.session_state.gst_pct / 100 if st.session_state.incl_gst else 0
    tq    = sum(i["qty"] for i in items)
    return gross, disc, net, gst, net+gst, tq

def to_excel_bytes():
    items = list(st.session_state.boq.values())
    gross, disc, net, gst_amt, grand, tq = boq_totals()
    rows = []
    for idx, item in enumerate(items, 1):
        siz = item["siz"]; sock = ""
        if item["cat"] == "PIPE":
            if "S/S" in siz: sock="S/S"; siz=siz.replace(" S/S","")
            elif "D/S" in siz: sock="D/S"; siz=siz.replace(" D/S","")
        rows.append({"Sr.":idx,"Series":item["series"],"Item Code":item["code"],
                     "Description":item["desc"],"DN":item["dn"],"Socket":sock,
                     "Size":siz if siz!="-" else "","Unit Price (Rs)":item["pr"],
                     "Qty":item["qty"],"Amount (Rs)":item["pr"]*item["qty"]})
    rows += [{}]
    rows += [{"Description":f"Project: {st.session_state.project_name}"},
             {"Description":f"Contractor: {st.session_state.contractor}"},
             {"Description":f"Date: {st.session_state.project_date}"},{}]
    rows.append({"Description":"Gross Total (Ex-GST)","Amount (Rs)":gross})
    if st.session_state.discount>0:
        rows.append({"Description":f"Discount @ {st.session_state.discount}%","Amount (Rs)":-round(disc)})
        rows.append({"Description":"Net Total (Ex-GST)","Amount (Rs)":round(net)})
    if st.session_state.incl_gst:
        rows.append({"Description":f"GST @ {st.session_state.gst_pct}%","Amount (Rs)":round(gst_amt)})
    rows.append({"Description":"GRAND TOTAL","Amount (Rs)":round(grand)})
    out = BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df = pd.DataFrame(rows)
        df.to_excel(w, sheet_name="BOQ", index=False)
        ws = w.sheets["BOQ"]
        for i, wd in enumerate([4,14,24,42,12,6,12,16,6,16],1):
            ws.column_dimensions[ws.cell(1,i).column_letter].width = wd
    return out.getvalue()

def import_excel(f):
    try:
        df = pd.read_excel(f)
        if not {"Item Code","Qty"}.issubset(set(df.columns)):
            return False,"Missing columns: Item Code, Qty"
        cmap = {p["code"]:p for p in ALL_PRODUCTS}
        new_boq={};count=0
        for _,row in df.iterrows():
            code=str(row.get("Item Code","")).strip()
            qty=int(row.get("Qty",0)) if pd.notna(row.get("Qty",0)) else 0
            if code and qty>0 and code in cmap:
                new_boq[code]=dict(cmap[code],qty=qty);count+=1
        if count: st.session_state.boq=new_boq; return True,f"Imported {count} items!"
        return False,"No matching items found."
    except Exception as e: return False,f"Error: {e}"

# ══════════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:#0a0e1a}
[data-testid="stHeader"]{background:#0a0e1a;border-bottom:1px solid #1e293b}
.block-container{padding:1rem 1.5rem 4rem!important;max-width:1400px}
div.stButton>button{width:100%;border-radius:10px;font-weight:700;transition:all .15s;
  border:2px solid #334155;background:#1e293b;color:#e2e8f0;padding:.45rem .3rem;font-size:12px}
div.stButton>button:hover{border-color:#3b82f6;background:#1e3a5f;color:#93c5fd;transform:translateY(-2px)}
div.stButton>button:active{transform:scale(.97)}
[data-testid="metric-container"]{background:#1e293b;border-radius:10px;padding:.75rem 1rem;border:1px solid #334155}
[data-testid="stMetricLabel"]{font-size:12px;color:#64748b}
[data-testid="stMetricValue"]{font-size:20px;color:#34d399;font-weight:800}
.sh{background:linear-gradient(90deg,#1e3a5f,#0a0e1a);border-left:4px solid #3b82f6;
    border-radius:4px;padding:8px 14px;margin-bottom:10px;color:#93c5fd;font-weight:700;font-size:14px}
.fh{background:linear-gradient(90deg,#3d2000,#0a0e1a);border-left:4px solid #f59e0b;color:#fcd34d}
.pc{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:8px 11px;margin-bottom:5px}
.hb{background:#7c2d12;color:#fdba74;font-size:10px;font-weight:700;padding:1px 6px;border-radius:4px;display:inline-block}
.ub{background:#1e3a5f;color:#7dd3fc;font-size:10px;font-weight:700;padding:1px 6px;border-radius:4px;display:inline-block}
.sb{background:#064e3b;color:#6ee7b7;font-size:10px;font-weight:700;padding:1px 6px;border-radius:4px;display:inline-block}
.db{background:#4c1d95;color:#c4b5fd;font-size:10px;font-weight:700;padding:1px 6px;border-radius:4px;display:inline-block}
.nb{background:#7c2d00;color:#fed7aa;font-size:9px;font-weight:700;padding:1px 5px;border-radius:3px;display:inline-block;margin-left:4px}
.cd{color:#64748b;font-size:11px;font-family:monospace}
.de{color:#e2e8f0;font-size:13px;font-weight:500}
.pr{color:#34d399;font-weight:700;font-size:13px}
[data-testid="stSidebar"]{background:#0f172a;border-right:1px solid #1e293b}
[data-testid="stExpander"]{background:#0d1424;border:1px solid #1e293b;border-radius:8px;margin-bottom:6px}
[data-testid="stTabs"] [data-baseweb="tab"]{background:#1e293b;border-radius:6px 6px 0 0;font-weight:600;color:#64748b;font-size:13px}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"]{background:#1e40af;color:white}
hr{border-color:#1e293b}
</style>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔧 Eze Plumbing BOQ")
    st.caption("Huliot HT Pro + Ultra Silent · **Apr 2026**")
    st.divider()
    st.markdown("**Project Info**")
    st.session_state.project_name = st.text_input("Project / Site Name", st.session_state.project_name, placeholder="Tower A – Block 3")
    st.session_state.contractor   = st.text_input("Contractor", st.session_state.contractor)
    st.session_state.project_date = st.date_input("Date", value=date.fromisoformat(st.session_state.project_date)).isoformat()
    st.divider()
    st.markdown("**Series Filter**")
    st.session_state.series_filter = st.radio("Show", ["Both","HT Pro","Ultra Silent"], horizontal=True)
    st.divider()
    st.markdown("**Pricing**")
    st.session_state.discount = st.number_input("Discount %", 0, 100, int(st.session_state.discount), 1)
    st.session_state.incl_gst = st.checkbox("Include GST", value=st.session_state.incl_gst)
    if st.session_state.incl_gst:
        st.session_state.gst_pct = st.number_input("GST %", 0, 28, int(st.session_state.gst_pct), 1)
    st.divider()
    st.markdown("**Import / Export**")
    uploaded = st.file_uploader("📤 Import BOQ Excel", type=["xlsx","xls"])
    if uploaded:
        ok, msg = import_excel(uploaded)
        st.success(msg) if ok else st.error(msg)
        if ok: st.rerun()
    if st.session_state.boq:
        gross,_,net,_,grand,tq = boq_totals()
        fname=f"{(st.session_state.project_name or 'BOQ').replace(' ','_')}_{st.session_state.project_date}.xlsx"
        st.download_button("📥 Export BOQ Excel", data=to_excel_bytes(), file_name=fname,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        st.divider()
        st.markdown(f"**Lines:** {len(st.session_state.boq)} | **Qty:** {tq}")
        st.markdown(f"**Net:** ₹{round(net):,}")
        if st.session_state.incl_gst: st.markdown(f"**Grand:** ₹{round(grand):,}")
        if st.button("🗑 Clear BOQ", use_container_width=True):
            st.session_state.boq={}; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
h1,h2,h3 = st.columns([1,4,3])
with h1:
    st.markdown('<div style="background:linear-gradient(135deg,#2563eb,#7c3aed);color:white;'
                'font-weight:900;font-size:28px;padding:10px 16px;border-radius:10px;'
                'text-align:center;letter-spacing:2px;">EZE</div>', unsafe_allow_html=True)
with h2:
    pool = get_pool()
    pipes = [p for p in pool if p["cat"]=="PIPE"]
    ss_n = sum(1 for p in pipes if "S/S" in p["siz"])
    ds_n = sum(1 for p in pipes if "D/S" in p["siz"])
    st.markdown(f'<div style="padding:6px 0">'
                f'<div style="font-size:19px;font-weight:800;color:#f1f5f9;">Plumbing Quantity Sheet</div>'
                f'<div style="font-size:11px;color:#475569;">Huliot <b style="color:#f97316">April 2026</b> · '
                f'Pipes: {ss_n} S/S + {ds_n} D/S = {len(pipes)} variants · '
                f'Other: {len(pool)-len(pipes)} items · Total: {len(pool)}</div></div>',
                unsafe_allow_html=True)
with h3:
    if st.session_state.boq:
        gross,_,net,_,grand,tq = boq_totals()
        m1,m2,m3 = st.columns(3)
        m1.metric("Lines", len(st.session_state.boq))
        m2.metric("Qty", tq)
        m3.metric("Net", f"₹{round(net):,}")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
#  CARD RENDERER
# ══════════════════════════════════════════════════════════════════════════════
# 2026 new items for highlighting
NEW_2026_CODES = {
    "42134050-i","7072134070-i","40754867-HM","41044857-HM","7070040877-i",
    "7070754877-i","7070764877-i","5401106650-i","540110502-i","5401105102-i","540110503-i",
    "14040764860-i",
}

def render_cards(items, prefix):
    n = 3
    for row in [items[i:i+n] for i in range(0,len(items),n)]:
        cols = st.columns(n)
        for j, p in enumerate(row):
            with cols[j]:
                hb = "hb" if p["series"]=="HT Pro" else "ub"
                sn = "HT" if p["series"]=="HT Pro" else "US"
                siz = p["siz"]; pbadge=""; sdisplay=siz if siz!="-" else ""
                if p["cat"]=="PIPE":
                    if "S/S" in siz: pbadge=' <span class="sb">S/S</span>'; sdisplay=siz.replace(" S/S","")
                    elif "D/S" in siz: pbadge=' <span class="db">D/S</span>'; sdisplay=siz.replace(" D/S","")
                new_badge=' <span class="nb">NEW 2026</span>' if p["code"] in NEW_2026_CODES else ""
                in_boq = p["code"] in st.session_state.boq
                qty_lbl = f" ×{st.session_state.boq[p['code']]['qty']}" if in_boq else ""
                dn_str = f'<span style="color:#64748b;font-size:11px;">DN {p["dn"]}</span>' if p["dn"]!="-" else ""
                sz_str = f' <span style="color:#64748b;font-size:11px;">· {sdisplay}</span>' if sdisplay else ""
                st.markdown(f"""<div class="pc">
                  <span class="{hb}">{sn}</span>{pbadge}{new_badge}
                  <span class="cd" style="margin-left:6px">{p['code']}</span><br/>
                  <span class="de">{p['desc']}</span><br/>
                  {dn_str}{sz_str}
                  <span class="pr" style="margin-left:6px">₹{p['pr']:,}{qty_lbl}</span>
                </div>""", unsafe_allow_html=True)
                if st.button(f"+ Add{qty_lbl}", key=f"{prefix}_{p['code']}", use_container_width=True):
                    add_to_boq(p); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
t1, t2, t3 = st.tabs(["📐 Dashboard", "🔍 Search", f"📋 BOQ ({len(st.session_state.boq)})"])

# ─── DASHBOARD ───────────────────────────────────────────────────────────────
with t1:
    pool = get_pool()
    pbdn = {}
    for p in pool:
        if p["cat"]=="PIPE":
            if p["dn"] not in pbdn: pbdn[p["dn"]]=[]
            pbdn[p["dn"]].append(p)

    st.markdown('<div class="sh">⬡ &nbsp; PIPES — Click DN tile · S/S & D/S both included</div>', unsafe_allow_html=True)
    avail = [d for d in PIPE_DNS if d in pbdn]
    if avail:
        tc = st.columns(len(avail))
        for i, dn in enumerate(avail):
            pipes_dn=pbdn[dn]
            ss_n=sum(1 for p in pipes_dn if "S/S" in p["siz"])
            ds_n=sum(1 for p in pipes_dn if "D/S" in p["siz"])
            active=st.session_state.active_pipe_dn==dn
            with tc[i]:
                lbl=f"DN {dn}\n{'▼' if active else '▶'}\nS/S:{ss_n} D/S:{ds_n}"
                if st.button(lbl, key=f"pdn_{dn}", use_container_width=True):
                    st.session_state.active_pipe_dn=None if active else dn
                    st.session_state.active_fit_cat=None
                    st.session_state.pipe_filter="Both"
                    st.rerun()

    if st.session_state.active_pipe_dn and st.session_state.active_pipe_dn in pbdn:
        dn=st.session_state.active_pipe_dn
        all_dn=pbdn[dn]
        ss_items=[p for p in all_dn if "S/S" in p["siz"]]
        ds_items=[p for p in all_dn if "D/S" in p["siz"]]
        fc1,fc2,fc3,_=st.columns([1,1,1,5])
        with fc1:
            if st.button("Both",key="pf_b"): st.session_state.pipe_filter="Both";st.rerun()
        with fc2:
            if st.button("S/S Only",key="pf_s"): st.session_state.pipe_filter="S/S";st.rerun()
        with fc3:
            if st.button("D/S Only",key="pf_d"): st.session_state.pipe_filter="D/S";st.rerun()

        def pipe_sort(p):
            for n,v in [("250",250),("500",500),("1000",1000),("1500",1500),("2000",2000),("3000",3000)]:
                if n in p["siz"]: return (v,0 if "S/S" in p["siz"] else 1)
            return (9999,0)

        pf=st.session_state.pipe_filter
        if pf=="S/S": show=sorted(ss_items,key=pipe_sort)
        elif pf=="D/S": show=sorted(ds_items,key=pipe_sort)
        else: show=sorted(all_dn,key=pipe_sort)

        with st.expander(f"DN {dn} — {len(show)} pipes [{pf}]", expanded=True):
            if show: render_cards(show, f"p{dn}")
            else: st.info(f"No {pf} pipes for DN {dn}.")

    st.divider()

    fbc={}
    for p in pool:
        if p["cat"]!="PIPE":
            if p["cat"] not in fbc: fbc[p["cat"]]=[]
            fbc[p["cat"]].append(p)

    st.markdown('<div class="sh fh">⚙ &nbsp; FITTINGS & ACCESSORIES — Click category to expand</div>', unsafe_allow_html=True)
    avail_fc=[fc for fc in FITTING_CATS if fc["key"] in fbc]
    for chunk in [avail_fc[i:i+8] for i in range(0,len(avail_fc),8)]:
        ccols=st.columns(len(chunk))
        for i,fc in enumerate(chunk):
            with ccols[i]:
                cnt=len(fbc[fc["key"]])
                active=st.session_state.active_fit_cat==fc["key"]
                lbl=f"{fc['emoji']}\n{fc['label']}\n{'▼' if active else '▶'} {cnt}"
                if st.button(lbl,key=f"fc_{fc['key']}",use_container_width=True):
                    st.session_state.active_fit_cat=None if active else fc["key"]
                    st.session_state.active_pipe_dn=None
                    st.rerun()

    if st.session_state.active_fit_cat and st.session_state.active_fit_cat in fbc:
        ck=st.session_state.active_fit_cat
        fc_info=next((f for f in FITTING_CATS if f["key"]==ck),{"emoji":"","label":ck})
        with st.expander(f"{fc_info['emoji']} {fc_info['label']} — {len(fbc[ck])} items", expanded=True):
            render_cards(fbc[ck],f"fit_{ck}")

# ─── SEARCH ──────────────────────────────────────────────────────────────────
with t2:
    sq=st.text_input("Search",placeholder="🔍 Type code, DN, description, S/S, D/S, category…",
                     key="sq",label_visibility="collapsed")
    if sq.strip():
        q=sq.lower()
        res=[p for p in get_pool() if any(q in str(p[k]).lower() for k in ["desc","code","dn","cat","siz","series"])][:60]
        st.caption(f"{len(res)} results for '{sq}'")
        if res: render_cards(res,"srch")
        else: st.info("No matching items.")
    else:
        pool=get_pool()
        pipes=[p for p in pool if p["cat"]=="PIPE"]
        ss_n=sum(1 for p in pipes if "S/S" in p["siz"])
        ds_n=sum(1 for p in pipes if "D/S" in p["siz"])
        st.markdown(f"""<div style="text-align:center;padding:40px 20px;color:#334155">
          <div style="font-size:40px;margin-bottom:10px">🔍</div>
          <div style="font-size:16px;font-weight:600;color:#475569">Search {len(pool)} products — April 2026 Prices</div>
          <div style="font-size:12px;margin-top:8px;color:#475569">
            Pipes: {ss_n} S/S + {ds_n} D/S = {len(pipes)} variants &nbsp;|&nbsp; Other: {len(pool)-len(pipes)} items
          </div>
          <div style="font-size:11px;margin-top:6px;color:#64748b">
            Try: "87.5" · "D/S" · "S/S" · "110" · "swept tee" · "smartlock" · "boss" · "new 2026"
          </div></div>""", unsafe_allow_html=True)

# ─── BOQ ─────────────────────────────────────────────────────────────────────
with t3:
    if not st.session_state.boq:
        st.markdown("""<div style="text-align:center;padding:80px 20px;color:#334155">
          <div style="font-size:48px;margin-bottom:12px">📋</div>
          <div style="font-size:17px;font-weight:600;color:#475569">BOQ is empty</div>
          <div style="font-size:13px;margin-top:8px">Use Dashboard or Search to add items</div>
        </div>""", unsafe_allow_html=True)
    else:
        gross,disc,net,gst_amt,grand,tq=boq_totals()
        m1,m2,m3,m4=st.columns(4)
        m1.metric("Lines",len(st.session_state.boq))
        m2.metric("Qty",tq)
        m3.metric("Gross",f"₹{round(gross):,}")
        m4.metric("Net",f"₹{round(net):,}")
        st.divider()

        items=list(st.session_state.boq.values())
        for idx,item in enumerate(items):
            ca,cb,cc,cd_,ce,cf,cg,ch=st.columns([.4,3.5,.8,1.2,1,.8,1.2,.5])
            with ca:
                st.markdown(f"<div style='color:#475569;font-size:12px;padding-top:8px'>{idx+1}</div>",unsafe_allow_html=True)
            with cb:
                hb="hb" if item["series"]=="HT Pro" else "ub"
                sn="HT" if item["series"]=="HT Pro" else "US"
                siz=item["siz"]; pb=""
                if "S/S" in siz: pb=' <span class="sb">S/S</span>'
                elif "D/S" in siz: pb=' <span class="db">D/S</span>'
                st.markdown(f"""<div style="padding-top:4px">
                  <span class="{hb}">{sn}</span>{pb}
                  <span class="cd" style="margin-left:6px">{item['code']}</span><br/>
                  <span class="de">{item['desc']}</span>
                </div>""",unsafe_allow_html=True)
            with cc:
                st.markdown(f"<div style='padding-top:8px;font-size:12px;color:#94a3b8'>DN {item['dn']}</div>",unsafe_allow_html=True)
            with cd_:
                sd=siz.replace(" S/S","").replace(" D/S","") if siz!="-" else "—"
                st.markdown(f"<div style='padding-top:8px;font-size:11px;color:#64748b'>{sd}</div>",unsafe_allow_html=True)
            with ce:
                st.markdown(f"<div style='padding-top:8px;font-size:12px;color:#94a3b8'>₹{item['pr']:,}</div>",unsafe_allow_html=True)
            with cf:
                nq=st.number_input("",min_value=0,max_value=9999,value=item["qty"],
                                   key=f"qty_{item['code']}",label_visibility="collapsed")
                if nq!=item["qty"]:
                    if nq==0: del st.session_state.boq[item["code"]]
                    else: st.session_state.boq[item["code"]]["qty"]=nq
                    st.rerun()
            with cg:
                st.markdown(f"<div style='padding-top:8px;font-size:13px;font-weight:700;color:#34d399;text-align:right'>₹{item['pr']*item['qty']:,}</div>",unsafe_allow_html=True)
            with ch:
                if st.button("✕",key=f"del_{item['code']}",use_container_width=True):
                    del st.session_state.boq[item["code"]]; st.rerun()
            if idx<len(items)-1:
                st.markdown("<hr style='margin:2px 0;border-color:#1e293b'>",unsafe_allow_html=True)

        st.divider()
        _,ct=st.columns([2,1])
        with ct:
            st.markdown(f"""<div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:20px 24px">
              <div style="font-size:11px;color:#f97316;font-weight:700;letter-spacing:1px;margin-bottom:12px">
                BOQ SUMMARY · APRIL 2026 PRICE LIST</div>
              <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="color:#94a3b8">Gross Total ({tq} qty)</span>
                <span style="color:#e2e8f0;font-weight:700">₹{round(gross):,}</span>
              </div>""",unsafe_allow_html=True)
            if st.session_state.discount>0:
                st.markdown(f"""<div style="display:flex;justify-content:space-between;margin-bottom:8px">
                  <span style="color:#94a3b8">Discount @ {st.session_state.discount}%</span>
                  <span style="color:#ef4444;font-weight:700">−₹{round(disc):,}</span>
                </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;border-top:1px solid #1e293b;padding-top:10px;margin-bottom:8px">
                <span style="color:#94a3b8;font-weight:700">Net Total (Ex-GST)</span>
                <span style="font-size:18px;font-weight:800;color:#34d399">₹{round(net):,}</span>
              </div>""",unsafe_allow_html=True)
            if st.session_state.incl_gst:
                st.markdown(f"""<div style="display:flex;justify-content:space-between;margin-bottom:8px">
                  <span style="color:#94a3b8">GST @ {st.session_state.gst_pct}%</span>
                  <span style="color:#94a3b8">+₹{round(gst_amt):,}</span>
                </div>
                <div style="display:flex;justify-content:space-between;border-top:1px solid #334155;padding-top:10px">
                  <span style="color:#e2e8f0;font-weight:800;font-size:14px">GRAND TOTAL</span>
                  <span style="font-size:20px;font-weight:900;color:#f97316">₹{round(grand):,}</span>
                </div>""",unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)
            st.caption("* List Price ex-factory/depot. Subject to trade discount. GST extra.")
            fname=f"{(st.session_state.project_name or 'BOQ').replace(' ','_')}_{st.session_state.project_date}.xlsx"
            st.download_button("📥 Download Excel BOQ",data=to_excel_bytes(),file_name=fname,
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True,type="primary")
