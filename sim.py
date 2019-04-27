from config import *


def standard_config() -> Config:
    config = Config()
    config.natural()
    return config


config = standard_config()

success = 0
fail = 0
for i in range(config.iterations):
    if i % config.report_every == 0:
        print('Iteration: {}'.format(i))
    board = config.new_board()
    if config.validate(board):
        success += 1
    else:
        fail += 1
