"""Configuration objects for the simulator.

A config is needed, which comes mostly populated with defaults.

You probably always want to use either natural() or change() on
the config.

You can use require_minimum() to set up a pretty standard search
criteria. If you want something more complicated, follow the
pattern there and configure your own requirement_validator.
"""

from collections import defaultdict
import random
from typing import List, Dict, Callable
import json

# List of all the colors and an arbitrary index value.
COLOR_MAP = {
    'r': 1, # Red
    'g': 2, # Green
    'b': 3, # Blue
    'l': 4, # Light
    'd': 5, # Dark
    'h': 6, # Heart
    'p': 7, # Poison
    'm': 8, # Mortal Poison
    'j': 9, # Jammer
    'o': 10, # Bomb
}

# Just the five attack colors.
NO_HEARTS = ['r', 'g', 'b', 'l', 'd']

# Five attack colors and hearts
STANDARD_COLORS = NO_HEARTS + ['h']

# Standard typedef for types and their count in a board.
CountsByType = Dict[str, int]


class Board(object):
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows

        self.board_state = [0] * (cols * rows)

    def counts_by_type(self) -> CountsByType:
        """Summary of orb counts by type."""
        counts = defaultdict(int)
        for x in self.board_state:
            counts[x] += 1
        return counts

    def any_matches(self, match_size: int) -> bool:
        """Returns true if any match is found."""
        for x in range(self.cols - match_size + 1):
            for y in range(self.rows):
                orb = self.orb_at(x, y)
                for x2 in range(x + 1, self.cols):
                    if orb != self.orb_at(x2, y):
                        break
                    if x2 - x + 1 >= match_size:
                        return True

        for y in range(self.rows - match_size + 1):
            for x in range(self.cols):
                orb = self.orb_at(x, y)
                for y2 in range(y + 1, self.rows):
                    if orb != self.orb_at(x, y2):
                        break
                    if y2 - y + 1 >= match_size:
                        return True

        return False

    def orb_at(self, col, row) -> int:
        return self.board_state[row * self.cols + col]

    def initialize(self, spawn_types: List[str]):
        for i in range(len(self.board_state)):
            self.board_state[i] = random.choice(spawn_types)

    def print_board(self):
        for y in range(self.rows):
            s = y * self.cols
            e = s + self.cols
            print(self.board_state[s:e])

class Config(object):
    def __init__(self):
        # Number of iterations to test.
        self.iterations = 50000
        # Print partial results this frequently.
        self.report_every = 25000

        # Board columns.
        self.board_cols = 6
        # Board rows.
        self.board_rows = 5

        # Used to confirm a randomly spawned board is acceptable.
        self.spawn_validator = AlwaysAccept()
        # Number of times to attempt to create a random board. This is set
        # excessively high; it should be pretty rare to hit this.
        self.spawn_attempts = 1000

        # Orb types to spawn, from the list in COLOR_MAP.
        self.spawn_types = []

        # The validator object which determines if a board matches the requirements.
        self.requirement_validator = AlwaysAccept()

    def natural(self, extra_types: List[str] = None):
        """Helper for setting up a natural spawn, with optional extra orb types."""
        types = set(STANDARD_COLORS)
        if extra_types:
            types.update(extra_types)
        self.spawn_types = list(types)
        self.spawn_validator = NaturalBoardSpawnValidator()

    def change(self, orb_types: List[str] = None):
        """Helper for setting up an orb change with specific orb types."""
        self.spawn_types = orb_types
        self.spawn_validator = OrbChangeSpawnValidator(orb_types)

    def require_minimum(self, minimum_counts: CountsByType):
        def remove_unused(input_counts: CountsByType):
            return {k: v for k, v in input_counts.items() if k in minimum_counts}

        def accept_minimum(input_counts: CountsByType):
            return all([input_counts.get(t, 0) >= v for t, v in minimum_counts.items()])

        self.requirement_validator = TrackingBoardValidator(accept_minimum,
                                                            transform_fn=remove_unused)

    def new_board(self) -> Board:
        """Initialize a new board based on the configuration."""
        for i in range(self.spawn_attempts):
            board = Board(self.board_cols, self.board_rows)
            board.initialize(self.spawn_types)
            if self.spawn_validator.validate(board):
                return board

        raise ValueError('Failed to create valid board in {} attempts'.format(self.spawn_attempts))

    def validate(self, board: Board) -> bool:
        return self.requirement_validator.validate(board)


class Validator(object):
    """Evaluates a board for some condition and returns True or False."""

    def validate(self, board: Board) -> bool:
        raise NotImplementedError()


class AlwaysAccept(Validator):
    """Dummy validator that always returns true."""

    def validate(self, board: Board) -> bool:
        return True


class StandardSpawnValidator(Validator):
    """Helper to determine if a board is acceptable.

    In general use either NaturalBoardSpawnValidator or OrbChangeSpawnValidator which
    will ensure that you configure things properly.
    """

    def __init__(self, accept_matches: bool, match_size: int, require_one: bool, spawn_types: List[str]):
        # If True, generated boards with matches (i.e. an active was used) are acceptable.
        # If False, no matches are allowed (natural boards).
        self.accept_matches = accept_matches
        # Number of orbs in a row to be considered a match. Only used if accept_matches == False.
        self.match_size = match_size
        # If true, at least one of each spawn_type must be selected for the board to
        # be valid. This is a standard pad feature for actives.
        self.require_one = require_one
        # Orb types that can spawn. Only used if require_one is set.
        self.spawn_types = spawn_types

    def validate(self, board: Board) -> bool:
        if not self.accept_matches:
            if board.any_matches(self.match_size):
                return False

        if self.require_one:
            counts = board.counts_by_type()
            one_match_each = all([counts[x] >= 3 for x in self.spawn_types])
            if not one_match_each:
                return False

        return True


class NaturalBoardSpawnValidator(StandardSpawnValidator):
    """Helper used for natural boards."""

    def __init__(self, match_size: int = 3):
        super().__init__(accept_matches=False,
                         match_size=match_size,
                         require_one=False,
                         spawn_types=[])


class OrbChangeSpawnValidator(StandardSpawnValidator):
    """Helper used for orb changes."""

    def __init__(self, spawn_types: List[str] = None):
        if not spawn_types:
            raise ValueError('Bad spawn_types')
        super().__init__(accept_matches=True,
                         match_size=0,
                         require_one=True,
                         spawn_types=spawn_types)


class TrackingBoardValidator(Validator):
    """Helper for building validators that keep track accepted board counts ."""

    def __init__(self,
                 accept_fn: Callable[[Dict[str, int]], bool],
                 transform_fn: Callable[[CountsByType], CountsByType] = lambda x: x):
        # Determines if the board configuration passes.
        # The transformation function is applied first.
        self.accept_fn = accept_fn

        # An optional user-provided function for transforming the counts of each type.
        # Applied before the accept_fn is run. Can be used to narrow down the tracked
        # results if you expect a lot of different permutations, and you aren't
        # interested in them.
        self.transform_fn = transform_fn

        # Tracking for transformed/accepted results.
        self.accepted_results =  defaultdict(int)

    def validate(self, board: Board) -> bool:
        counts = board.counts_by_type()
        counts = self.transform_fn(counts)
        if self.accept_fn(counts):
            self.accepted_results[self._flatten_counts(counts)] += 1
            return True
        return False

    def _flatten_counts(self, counts) -> str:
        return json.dumps(counts, sort_keys=True)
