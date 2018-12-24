from unittest import TestCase

from envs.tictactoe_env import Board, X, O


class TestBoard(TestCase):
    def test_blanks(self):
        board = Board()
        self.assertEqual(set(range(board.size)), board.blanks)

        non_blanks = set()
        for pos in range(board.size):
            board[pos] = X
            non_blanks.add(pos)

            intersection = non_blanks.intersection(board.blanks)
            self.assertEqual(len(intersection), 0)

            union = non_blanks.union(board.blanks)
            self.assertEqual(len(union), board.size)

    def test_is_full(self):
        empty_board = Board()
        self.assertFalse(empty_board.is_full())

        board = Board()

        blanks = board.blanks
        pos = blanks.pop()
        while len(board.blanks) > 1:
            board[pos] = X if pos % 2 == 0 else O
            self.assertFalse(board.is_full())
            pos = blanks.pop()

        board[pos] = O
        self.assertTrue(board.is_full())
    #
    # def test_is_empty(self):

    #     empty_board = Board()
    #     self.assertTrue(empty_board.is_empty())
    #
    #     board = Board()
    #     for pos in range(board.size ** 2):
    #         board[pos] = X if pos % 2 == 0 else O
    #         self.assertFalse(board.is_empty())
    #
    # def test_has_winner(self):
    #
    #     # Scenario 1: blank board has no winner
    #     self.assertFalse(Board().has_winner())
    #
    #     # Scenario 2: winning on row
    #     for i in range(3):
    #         board = Board()
    #
    #         board[i * board.size] = X
    #         board[i * board.size + 1] = X
    #         board[i * board.size + 2] = X
    #
    #         self.assertTrue(board.has_winner())
    #
    #     # Scenario 3: winning on column
    #     for i in range(3):
    #         board = Board()
    #
    #         board[i] = X
    #         board[i + board.size] = X
    #         board[i + 2 * board.size] = X
    #
    #         self.assertTrue(board.has_winner())
    #
    #     # Scenario 4: winning on diagonals
    #     board = Board()
    #
    #     board[0] = X
    #     board[4] = X
    #     board[8] = X
    #
    #     self.assertTrue(board.has_winner())
    #
    #     board = Board()
    #
    #     board[2] = X
    #     board[4] = X
    #     board[6] = X
    #
    #     self.assertTrue(board.has_winner())

    # def test_is_draw(self):
    #     self.fail()
