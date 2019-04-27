from config import *
import unittest


class TestBoards(unittest.TestCase):

    def test_orb_at(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]

        self.assertEqual(b.orb_at(0, 0), 0)
        self.assertEqual(b.orb_at(5, 0), 5)
        self.assertEqual(b.orb_at(0, 1), 6)
        self.assertEqual(b.orb_at(5, 1), 11)
        self.assertEqual(b.orb_at(5, 4), 29)

    def test_nomatch(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertFalse(b.any_matches(3))


    def test_match00h(self):
        b = Board(6, 5)
        b.board_state = [
             0,  0,  0,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertTrue(b.any_matches(3))

    def test_match00v(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             0,  7,  8,  9, 10, 11,
             0, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertTrue(b.any_matches(3))

    def test_0eh(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  5,  5,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertTrue(b.any_matches(3))

    def test_0ev(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10,  5,
            12, 13, 14, 15, 16,  5,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertTrue(b.any_matches(3))

    def test_3ev(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 17,
            24, 25, 26, 27, 28, 17,
        ]
        self.assertTrue(b.any_matches(3))

    def test_5eh(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 27, 27,
        ]
        self.assertTrue(b.any_matches(3))

    def test_0h_broken(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  0,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertFalse(b.any_matches(3))

    def test_0v_broken(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
             0, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertFalse(b.any_matches(3))

    def test_eh_broken(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 27,
        ]
        self.assertFalse(b.any_matches(3))

    def test_match4(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  1,  1,  1,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertTrue(b.any_matches(4))

    def test_match4_only3(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  1,  8,  9, 10, 11,
            12,  1, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29,
        ]
        self.assertFalse(b.any_matches(4))

    def test_match4_broken(self):
        b = Board(6, 5)
        b.board_state = [
             0,  1,  2,  3,  4,  5,
             6,  7,  8,  9, 10, 11,
            12, 13, 14, 15, 16, 11,
            18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 11,
        ]
        self.assertFalse(b.any_matches(4))


if __name__ == '__main__':
    unittest.main()
