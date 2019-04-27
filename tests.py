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


def standard():
    config = standard_config()
    return config, 'standard, should be 100%'


def fire3natural():
    config = standard_config(minimum_counts={'r': 3})
    return config, 'Require 3 fire, natural board'


def fire3change():
    config = standard_config(natural=False, minimum_counts={'r': 3})
    return config, 'Require 3 fire, orb change'


def fire3heart3natural():
    config = standard_config(minimum_counts={'r': 3, 'h': 3})
    return config, 'Require 3 fire 3 heart, natural board'

def fire3heart3change():
    config = standard_config(natural=False, minimum_counts={'r': 3, 'h': 3})
    return config, 'Require 3 fire 3 heart, orb change'


def reiwa_configs():
    sizes = [(5, 6), (6, 7)]
    boards = [
        ('5-color', NO_HEARTS),
        ('reiwa-color', ['r', 'b', 'g', 'l'])
    ]
    requirements = {'r': 4, 'b': 4, 'g': 4, 'l': 4}

    configs = []
    for size in sizes:
        for board in boards:
            desc = 'reiwa {}x{} {}'.format(size[0], size[1], board[0])
            config = standard_config(natural=False, orb_types=board[1], minimum_counts=requirements)
            config.board_rows = size[0]
            config.board_cols = size[1]
            configs.append((desc, config))
    return configs

