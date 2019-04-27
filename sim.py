from config import *


def standard_config(natural=True, orb_types=None, minimum_counts=None) -> Config:
    config = Config()
    orb_types = orb_types or STANDARD_COLORS
    if natural:
        config.natural()
        config.spawn_types = orb_types
    else:
        config.change(orb_types)

    minimum_counts = minimum_counts or {}
    config.require_minimum(minimum_counts)

    return config

def run_test(config: Config, print_tracking_info: bool = False):
    success = 0
    fail = 0
    for i in range(config.iterations):
        if i > 0 and i % config.report_every == 0:
            print('Iteration {}: {} success {} fail'.format(i, success, fail))
        board = config.new_board()
        if config.validate(board):
            success += 1
        else:
            fail += 1

    print('Done: {} success {} fail, {:.2%}'.format(success, fail, success / (success + fail)))

    if print_tracking_info:
        for orbs, counts in config.requirement_validator.accepted_results.items():
            print(orbs, counts)


print('standard, should be 100%')
config = standard_config()
run_test(config)

print()
print('Require 3 fire')
config = standard_config(minimum_counts={'r': 3})
run_test(config)

print()
print('Require 3 fire, orb change')
config = standard_config(natural=False, minimum_counts={'r': 3})
run_test(config)


print()
print('Require 3 fire 3 heart')
config = standard_config(minimum_counts={'r': 3, 'h': 3})
run_test(config)

print()
print('Require 3 fire 3 heart, orb change')
config = standard_config(natural=False, minimum_counts={'r': 3, 'h': 3})
run_test(config)
