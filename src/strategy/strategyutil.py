from collections import OrderedDict
import numpy as np
import datautil as du
import math

def get_entropy(l):
    l_sum = np.sum(l)
    l_norm = [x/l_sum for x in l]
    entropy = -np.sum([x*math.log2(x) for x in l_norm if x > 0])
    return entropy

def gen_schedule(map_data, cfg):
    schedules = OrderedDict()

    for interID, inter in enumerate(map_data.intersection):
        st_ratio = inter.get_incoming_weight_normed()
        sch = OrderedDict()
        period = 0
        for st_name, ratio in st_ratio.items():
            rate = int(round(ratio * cfg['period']))
            if (map_data.street[st_name].cars_passed > 0) & (rate == 0):
                sch[st_name] = 1
            else:
                sch[st_name] = rate

            period += sch[st_name]

        if period == 0:
            for st_name, _ in sch.items():
                sch[st_name] = 1

        schedules[interID] = sch

    return schedules

def update_schedule(map_data, cfg, schedule_old = None):
    schedules = schedule_old
    inter_entropy = {}

    for interID, inter in enumerate(map_data.intersection):
        st_ratio = inter.get_incoming_weight_normed()
        inter_entropy[interID] = get_entropy(list(st_ratio.values()))

    inter_entropy = {k: v for k, v in sorted(inter_entropy.items(), key=lambda item: -item[1])[:10]}

    for interID, entropy in inter_entropy.items():
        inter = map_data.intersection[interID]
        st_ratio = inter.incoming_weight_normed
        ratio_max = max([x for x in list(st_ratio.values()) if x > 0.0] + [-1])
        for st_name, ratio in st_ratio.items():
            if ratio == ratio_max:
                schedules[interID][st_name] += 1

            period += sch[st_name]

        if period == 0:
            for st_name, _ in sch.items():
                sch[st_name] = 1

        schedules[interID] = sch

    return schedules
