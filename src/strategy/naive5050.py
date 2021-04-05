from collections import OrderedDict
import numpy as np

import strategy.strategyutil as su
import datautil as du

# find all intersection then divide car flow
def validate(cfg):
    assert ('period' in cfg.keys())

def gen_schedule(map_data, cfg):

    for interID, inter in enumerate(map_data.intersection):
        for st_name in inter.incoming:
            inter.incoming_weight[st_name].append(1)

    return su.gen_schedule(map_data, cfg)
