#!/bin/bash

###########
# IMPORTS #
###########

import os
import folium
import mailbox
from folium.plugins import HeatMap


################
# DICTIONARIES #
################

# Match email domains etc to college id
matches = {
    "flsouthern.edu": "fl_southern",
    "butler.edu": "butler",
    "ncat.edu": "nc_at",
    "wfu.edu": "wake_forest",
    "ou.edu": "ou",
    "tulane.edu": "tulane",
    "rhodes.edu": "rhodes",
    "wlu.edu": "wash-lee",
    "champlain.edu": "champlain",
    "xavier.edu": "xavier",
    "pitt.edu": "pitt",
    "vcu.edu": "vcu",
    "misericordia.edu": "misery",
    "miamioh": "oh_miami",
    "unf.edu": "unf",
    "smu.edu": "smu",
    "shuadmissions.org": "seton-hall",
    "centre.edu": "centre",
    "unca.edu": "unc_a",
    "Concord University Admissions": "concord",
    "winthrop.edu": "winthrop",
    "fit.edu": "fl_tech",
    "highpoint.edu": "nc_hpu",
    "lynchburg.edu": "lynchburg",
    "usfca.edu": "ca_sf",
    "siu.edu": "siu",
    "cofc.edu": "charleston",
    "colgate.edu": "colgate",
    "drexel.edu": "drexel",
    "arcadia.edu": "arcadia",
    "belmont.edu": "belmont",
    "mercer.edu": "mercer",
    "colby.edu": "colby",
    "catawba": "catawba",
    "smcm.edu": "st-mary",
    "babson.edu": "babson",
    "hsc.edu": "hampden-syd",
    "applyferrum.org": "ferrum",
    "depauw.edu": "depauw",
    "ecu.edu": "nc_ecu",
    "liu.edu": "long-island",
    "mhu.edu": "mars-hill",
    "queens.edu": "queens",
    "kettering.edu": "kettering",
    "vwu.edu": "va_wes",
    "wittenberg.edu": "wittenberg",
    "ncsu.edu": "nc_state",
    "wingateinfo.org": "wingate",
    "furman.edu": "furman",
    "fontbonne.edu": "fontbonne",
    "utdallas.edu": "tx_dal",
    "gmu.edu": "george-mason",
    "bucknell.edu": "bucknell",
    "brown.edu": "brown",
    "roanoke.edu": "roanoke",
    "indiana.edu": "ia",
    "uvm.edu": "vt",
    "insidewcu": "nc_wcu",
    "uga.edu": "ga",
    "elon.edu": "elon",
    "uncg.edu": "unc_g",
    "guilford.edu": "guilford",
    "trinity.edu": "trinity",
    "uat.edu": "uat",
    "cn.edu": "carson-newman",
    "rit.edu": "rit",
    "umd.edu": "md",
    "simons-rock.edu": "simons-rock",
    "unc.edu": "unc_ch",
    "davidson.edu": "davidson",
    "colorado.edu": "colorado",
    "uncc.edu": "uncc",
    "appstate.edu": "app",
    "uncw.edu": "uncw",
    "concord.edu": "concord",
    "shu.edu": "seton-hall",
    "durhamtech.edu": "durham-tech",
    "DURHAMTECH.EDU": "durham-tech",

    "discovermercer.com": "mercer",  # ?
    "smcm-admissions.org": "st-mary",  # ?
    "gmu.envisionexperience.com": "george-mason",  # ?
    "shuadmission.org": "seton-hall",
    "MiamiOH.edu": "oh_miami",  # ?
    "hsc-admissions.org": "hampden-syd",
    "yourmomentatbabson.net": "babson",
    """University of Virginia" <no-reply@m.mail.coursera.org>""": "uva",
    "go-unccharlotte.org": "uncc",
    """North Carolina State University <admin@em.mycollegeoptions.org>""": "nc_state",
    "ncat.email": "nc_at",
    "Hampden-SydneyVA.org": "hampden-syd",
    "info.ferrum.edu": "ferrum",
    "explorehsc": "hampden-syd",

    "btate@thefinancialclinic.org": "durham-tech",  # DT finance help
    """Duke University" <no-reply@m.mail.coursera.org>""": "duke",  # Duke TIP
    "e.collegeboard.org": "",  # Collegeboard
    "nshss.org": "",  # NSHSS
}

# Locations of colleges
# Taken from coordinates of OSM object
college_coords = {
    "": [0, 0],  # unknown
    "fl_southern": [28.0312033, -81.9461962],  # w113525303
    "butler": [39.8409860, -86.1717615],  # w347368393
    "nc_at": [36.0768424, -79.7720437],  # w479968151
    "wake_forest": [36.1334952, -80.2759330],  # w31270748
    "ou": [35.1963347, -97.4425441],  # w392003756
    "tulane": [29.9412060, -90.1194141],  # w27892131
    "rhodes": [35.1556820, -89.9889328],  # w105091408
    "wash-lee": [37.7923838, -79.4454645],  # w232826024
    "champlain": [44.4741657, -73.2047025],  # r3516260
    "xavier": [39.1499039, -84.4721957],  # r2271876
    "pitt": [40.4438959, -79.9581739],  # r2079309
    "vcu": [37.5481009, -77.4512784],  # w246742439
    "misery": [41.3457119, -75.9725878],  # n357298148
    "oh_miami": [39.5078927, -84.7302237],  # w183831887
    "unf": [30.2685535, -81.5070993],  # w420815429
    "smu": [32.8424015, -96.7819568],  # w30894474
    "seton-hall": [40.7427920, -74.2462031],  # w37684708
    "centre": [37.6439346, -84.7811679],  # n358584610,
    "unc_a": [35.6161500, -82.5661293],  # w205858867
    "concord": [37.4256082, -81.0063834],  # w392029324
    "winthrop": [34.9392126, -81.0323395],  # w256490835
    "fl_tech": [28.0638216, -80.6230338],  # w282186715
    "nc_hpu": [35.9717985, -79.9960328],  # n6459601060
    "lynchburg": [37.3985094, -79.1835829],  # w427914658
    "ca_sf": [37.7778066, -122.4509497],  # r5996294
    "siu": [38.7929771, -89.9963543],  # w468699691
    "charleston": [32.7842025, -79.9376102],  # w490220969
    "colgate": [42.8151172, -75.5399221],  # w344307894
    "drexel": [39.9570387, -75.1881635],  # w49991637
    "arcadia": [40.0920284, -75.1659531],  # w30647419
    "belmont": [36.1323017, -86.7930747],  # w185564024
    "mercer": [32.8318060, -83.6499029],  # n358692163
    "colby": [44.5646770, -69.6617937],  # w39754167
    "catawba": [35.6916143, -80.4855296],  # w475576329
    "st-mary": [38.1893975, -76.4255320],  # w311346875
    "babson": [42.2954266, -71.2664229],  # w588785843
    "hampden-syd": [37.2431501, -78.4585087],  # w183220577
    "ferrum": [36.9315027, -80.0248820],  # r7122416
    "depauw": [39.6397676, -86.8616760],  # n358676407
    "nc_ecu": [35.5989176, -77.3672884],  # r9950699
    "long-island": [40.8150440, -73.5908065],  # w94918526
    "mars-hill": [35.8269193, -82.5534578],  # w654381844
    "queens": [35.1885066, -80.8328829],  # w206288382
    "kettering": [43.0140081, -83.7081841],  # w609395450
    "va_wes": [36.8679279, -76.1881271],  # w377683884
    "wittenberg": [39.9351682, -83.8130296],  # r1867030
    "nc_state": [35.7664, -78.6753],  # r6431764
    "wingate": [34.9888294, -80.4420315],  # r8369265
    "furman": [34.9254022, -82.4392179],  # r4139356
    "fontbonne": [38.6416289, -90.3156811],  # w153089317
    "tx_dal": [32.9868275, -96.7503466],  # r7316239
    "george-mason": [38.8315024, -77.3122160],  # w337509448
    "bucknell":  [40.9542269, -76.8857764],  # r7213704
    "brown": [41.8265680, -71.4016441],  # w40877239
    "roanoke": [37.2954920, -80.0517680],  # r2207728
    "ia": [39.1762993, -86.5167524],  # w74173036
    "vt": [44.4757772, -73.1913420],  # r1610005
    "nc_wcu": [35.3085934, -83.1924881],  # r8408116
    "ga":  [33.9388755, -83.3709242],  # r7301023
    "elon": [36.1054, -79.5046],  # r6442121
    "unc_g": [36.0686, -79.8103],  # w479967959
    "guilford": [36.0951, -79.8850],  # w479968920
    "trinity": [29.4621975, -98.4833632],  # w593227006
    "uat": [33.3775270, -111.9758960],  # n723485085
    "carson-newman": [36.1214778, -83.4898960],  # n356843912
    "rit": [43.0823692, -77.6721972],  # w102645121
    "md": [38.9915448, -76.9467773],  # w488114799
    "simons-rock": [42.2079282, -73.3768287],  # w29785117
    "colorado": [40.0070979, -105.2664790],  # w46226108
    "uncc": [35.3068944, -80.7362618],  # w168664114
    "app": [36.2138, -81.6870],  # w510644856
    "unc_ch": [35.9042, -79.0480],  # r2882828
    "davidson": [35.5017, -80.8422],  # w568333555
    "uva": [37.9900051, -78.4756556],  # r4218705

    "durham-tech": [35.9753, -78.8819],  # r8047924
    "duke": [36.0019693, -78.9361207],  # r7407432

    "uncw": [34.2240, -77.8671],  # r7126636
    "nc_central": [35.9741, -78.8982],  # w49736769
    "bennett": [36.0672167, -79.7794315],  # w479968294
}


##############
# PROCESSING #
##############

counts = dict()

# Ingest mbox file
mbox = mailbox.mbox('Colleges.mbox')
# Lock mbox file to prevent damage, even though we're not editing
mbox.lock()


# HEATMAP STUFF

try:
    for message in mbox:
        found = False
        for cn in matches:
            if cn in message['from']:
                found = True
                try:
                    counts[matches[cn]] += 1
                except KeyError:
                    counts[matches[cn]] = 1
                break
        if not found:
            print(message['from'])
finally:
    mbox.unlock()

# print(counts)
# quit()

amounts = []
for i in counts:
    amounts.append(counts[i])

data = []

for c in counts:
    xx = college_coords[c]
    incoming = [xx[0], xx[1], counts[c]]
    data.append(incoming)

max_amount = float(max(amounts))

# print(data)
# quit()


###########
# HEATMAP #
###########

m = folium.Map(location=[40, -91], zoom_start=4)

HeatMap(data,
        # radius=20,
        # blur=14,
        min_opacity=0.25,
        max_zoom=3,
        max_val=max_amount
        ).add_to(m)

m.save(os.path.join('results', 'heatmap.html'))
