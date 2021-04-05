from collections import OrderedDict
import numpy as np
import datautil as du
import strategy.strategyutil as su
import util as u
import strategy.naiveratio_isa as nri
import sim
# find all intersection then divide car flow
def validate(cfg):
    assert ('iterations' in cfg.keys())

def gen_schedule(map_data, cfg):
    print(cfg)
    # init the schedule with the naiveratio strategy
    nri.validate(cfg['naiveratio']['config'])
    schedule = nri.gen_schedule(map_data, cfg['naiveratio']['config'])

    for i in range(cfg['iterations']):
        u.log_section(f'{i}-th Simulation Starts')
        loss_total, score, arrived = sim.run(map_data, schedule)
        u.log_section(f'{i}-th Simulation Ends')
        u.print_score(loss_total, score, len(arrived), map_data.misc.trip_count)

        for st_name, st in map_data.street.items():
            map_data.intersection[st.end].incoming_weight[st_name].append(sum(st.loss))
        schedule = su.update_schedule(map_data, cfg, schedule)

    return schedule
