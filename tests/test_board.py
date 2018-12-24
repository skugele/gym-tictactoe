from unittest import TestCase

from envs.tictactoe_env import Board, X


class TestBoard(TestCase):
    # def test_blanks(self):
    #     self.fail()
    #
    # def test_is_full(self):
    #     self.fail()
    #
    # def test_is_empty(self):
    #     self.fail()

    def test_has_winner(self):

        # Scenario 1: blank board has no winner
        self.assertFalse(Board().has_winner())

        # Scenario 2: winning on row
        for i in range(3):
            board = Board()

            board[i * board.size] = X
            board[i * board.size + 1] = X
            board[i * board.size + 2] = X

            self.assertTrue(board.has_winner())

        # Scenario 3: winning on column
        for i in range(3):
            board = Board()

            board[i] = X
            board[i + board.size] = X
            board[i + 2*board.size] = X

            self.assertTrue(board.has_winner())

        # Scenario 4: winning on diagonal
        board = Board()

        board[0] = X
        board[4] = X
        board[8] = X

        self.assertTrue(board.has_winner())

    # def test_is_draw(self):
    #     self.fail()
