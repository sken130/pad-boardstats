from config import *
import tests


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

test_list = [
    # tests.standard(),
    # tests.fire3natural(),
    # tests.fire3change(),
    # tests.fire3heart3natural(),
    # tests.fire3heart3change(),
]

test_list.extend(tests.reiwa_configs())

for t in test_list:
    print(t[0])
    run_test(t[1])
    print()

