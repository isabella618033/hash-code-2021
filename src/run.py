import argparse
import yaml

import datautil as du
import util as u
import strategy.naiveratio as nr
import strategy.naiveratio_isa as nri
import strategy.naive5050 as n5050
import strategy.iterative as it
import sim

def prepare_config():
    parser = argparse.ArgumentParser(description='traffic simulation')
    parser.add_argument('-c', '--cfg', help='File path config file', required=True)
    args = parser.parse_args()

    with open(args.cfg, 'r') as cfg_file:
        return yaml.load(cfg_file, Loader=yaml.FullLoader)

def gen_schedule(strategy, map_data):
    if strategy['name'] == 'naiveratio':
        nr.validate(strategy['config'])
        return nr.gen_schedule(map_data, strategy['config'])

    if strategy['name'] == 'naiveratio_isa':
        nri.validate(strategy['config'])
        return nri.gen_schedule(map_data, strategy['config'])

    if strategy['name'] == 'naive5050':
        n5050.validate(strategy['config'])
        return n5050.gen_schedule(map_data, strategy['config'])

    if strategy['name'] == 'iterative':
        it.validate(strategy['config'])
        return it.gen_schedule(map_data, strategy['config'])

def print_map_info(misc):
    print('Duration: {}'.format(misc.d))
    print('Intersections: {}'.format(misc.int_count))
    print('Streets: {}'.format(misc.str_count))
    print('Cars: {}'.format(misc.trip_count))
    print('Bonus: {}'.format(misc.f))

def main():
    u.log_section('Run Start')
    u.log_section('Prepare Config')
    cfg = prepare_config()
    print(cfg)

    dm = du.DataManager(cfg['map_path'], f"{cfg['schedule_path']}/{cfg['strategy']['name']}.in", f"{cfg['result_path']}/{cfg['strategy']['name']}.yaml", cfg['strategy']['config']['learning_rate'])
    dm.check_path()

    u.log_section('Load Map Data')
    map_data = dm.load_map(cfg['trip_count_max'])
    print_map_info(map_data.misc)

    u.log_section('Generate Schedule')
    schedule = gen_schedule(cfg['strategy'], map_data)
    dm.save_schedule(schedule)

    u.log_section('Simulation Starts')
    loss_total, score, arrived = sim.run(map_data, schedule)
    u.log_section('Simulation Ends')
    dm.save_result(score, arrived)
    u.print_score(loss_total, score, len(arrived), map_data.misc.trip_count)

    u.log_section('Run End')

if __name__ == "__main__":
    main()
