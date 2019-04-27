from collections import defaultdict

from typing import List

COLOR_MAP = {
    'r': 1,
    'g': 2,
    'b': 3,
    'l': 4,
    'd': 5,
    'h': 6,
    'p': 7,
    'm': 8,
    'j': 9,
    'o': 10,
}

STANDARD_COLORS = ['r', 'g', 'b', 'l', 'd', 'h']
NO_HEARTS = ['r', 'g', 'b', 'l', 'd']


class Board(object):
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows

        self.board_state = [0] * (cols * rows)

    def counts_by_type(self) -> defaultdict[str, int]:
        """Summary of orb counts by type."""
        counts = defaultdict(int)
        for x in self.board_state:
            counts[x] += 1
        return counts

    def matches_by_type(self):
        """Finds any matches in the board and reports them."""
        pass

    def initialize(self, spawn_types: List[str]):
        pass


class Config(object):
    def __init__(self):
        # Number of iterations to test.
        self.iterations = 10000
        # Print partial results this frequently.
        self.report_every = 1000

        # Board columns.
        self.board_cols = 6
        # Board rows.
        self.board_rows = 5

        self.spawn_validator = AlwaysAccept()

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

    def new_board(self) -> Board:
        for i in range(1000):
            board = Board(self.board_cols, self.board_rows)
            board.initialize(self.spawn_types)
            if self.spawn_validator.validate(board):
                return board
        raise ValueError('Failed to create valid board in {} attempts'.format(i))

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
            raise NotImplementedError()

        if self.require_one:
            counts = board.counts_by_type()
            all_present = all([counts[x] for x in self.spawn_types])
            if not all_present:
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
