import os, subprocess, time, signal
import random

import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import numpy as np

import logging

logger = logging.getLogger(__name__)


class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, size=3):
        self._size = size
        self._board = None
        self._done = False
        self._n_moves = 0

        # reward values
        self.win_reward = 1
        self.lose_reward = -1
        self.draw_reward = 0

        # actions
        self.action_space = spaces.Discrete(self._size ** 2)

        # observations
        self.observation_space = spaces.Box(low=np.array([-2] * (self._size ** 2)),
                                            high=np.array([1] * (self._size ** 2)),
                                            dtype=np.int64)

    def step(self, action):

        reward = 0

        info = {
            'board': str(self._board),
            'done': str(self._done),
            'comment:': 'none'
        }

        # Check if current state is terminal, if so then return warning
        if self._done:
            logger.warning(
                """
                You are calling 'step()' even though this environment has already returned done = True. 
                You should always call 'reset()' once you receive 'done = True' -- any further steps are 
                undefined behavior.
                """
            )

            info['comment'] = 'post-game action'

            return self._board.asarray(), reward, self._done, info

        # Verify legal action -- action compatible with current board
        elif action not in self._board.blanks:

            # TODO: Should this return a negative reward?
            logger.warning('Illegal action: ({})'.format(action))

            info['comment'] = 'illegal action'

        else:
            # update board with player's action
            self._board[action] = X

            # check if player won
            if self._board.has_winner():

                reward = self.win_reward
                self._done = True

                info['comment'] = 'player wins'

            elif self._board.is_full():

                reward = self.draw_reward
                self._done = True

                info['comment'] = 'draw'

            # add opponent's action
            else:

                opponent_action = random.choice(self._board.blanks)
                self._board[opponent_action] = O

                # check if opponent won
                if self._board.has_winner():
                    reward = self.lose_reward
                    self._done = True

                    info['comment'] = 'opponent wins'

        info['board'] = str(self._board)
        info['done'] = self._done

        return self._board.asarray(), reward, self._done, info

    def reset(self):
        self._board = Board()
        self._done = False

    def render(self, mode='human', close=False):
        print(self._board)


BLANK = 0
X = 1
O = -1


class Board(object):

    def __init__(self, shape=(3, 3)):
        self._board = np.ones(shape) * BLANK
        self._mark_dict = {BLANK: ' ', X: 'X', O: 'O'}

    @property
    def blanks(self):
        return set(np.ravel_multi_index(np.where(self._board == BLANK), self._board.shape))

    @property
    def size(self):
        return self._board.size

    def __getitem__(self, pos):
        return self._board[pos]

    def __setitem__(self, pos, mark):
        if mark not in [BLANK, X, O]:
            raise ValueError

        self._board[np.unravel_index(pos, self._board.shape)] = mark

    def __repr__(self):
        return str(self._board)

    def __str__(self):
        return self.board_string()

    def __eq__(self, other):
        return self._board == other._board

    def board_string(self):
        placeholder_rows = []
        for row in range(self._board.shape[0]):
            placeholder_rows.append('|'.join(['{}'] * self._board.shape[1]) + '\n')

        template = '─┼─┼─\n'.join(placeholder_rows)
        marks = [self._mark_dict[m] for m in np.nditer(self._board)]

        return template.format(*marks)

    def is_full(self):
        return BLANK not in self._board

    def is_empty(self):
        return (X not in self._board) and (O not in self._board)

    def asarray(self):
        return np.reshape(self._board, -1)

    def has_winner(self):
        # sum of board elements along rows
        row_sums = list(np.sum(self._board, 0))

        # sum of board elements along columns
        col_sums = list(np.sum(self._board, 1))

        # sum of elements along diagonals
        diag_sums = [np.sum(np.diag(self._board)), np.sum(np.diag(np.flip(self._board, axis=1)))]

        return True in (self._board.shape[0] == np.abs(row_sums + col_sums + diag_sums))

    def is_draw(self):
        return self.is_full() and not self.has_winner()
