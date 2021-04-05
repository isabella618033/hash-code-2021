from collections import OrderedDict
import numpy as np
import datautil as du
import strategy.strategyutil as su

# find all intersection then divide car flow
def validate(cfg):
    assert ('period' in cfg.keys())

def gen_schedule(map_data, cfg):

    for st_name, st in map_data.street.items():
        map_data.intersection[st.end].incoming_weight[st_name].append(st.cars_passed)

    return su.gen_schedule(map_data, cfg)
