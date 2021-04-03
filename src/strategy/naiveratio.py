from collections import OrderedDict
import numpy as np

import datautil as du


# find all intersection then divide car flow
def validate(cfg):
    assert ('period' in cfg.keys())

def gen_schedule(map_data, cfg):
    count_per_inter = []
    schedules = []

    for i in range(0, map_data.misc.int_count):
        count_per_inter.append({})

    for st_name, st in map_data.street.items():
        count_per_inter[st.end][st_name] = 0

    for c in map_data.trip:
        for st_name in c.path:
            st = map_data.street[st_name]
            count_per_inter[st.end][st_name] += 1

    for i in range(0, map_data.misc.int_count):
        s = sum(count_per_inter[i].values())
        sch = OrderedDict()
        for st_name, trip_count in count_per_inter[i].items():
            if s == 0:
                sch[st_name] = 0
            else:
                rate = int(round(trip_count / s * cfg['period']))
                if trip_count > 0 and rate == 0:
                    sch[st_name] = 1
                else:
                    sch[st_name] = rate

        schedules.append(sch)
    return schedules
