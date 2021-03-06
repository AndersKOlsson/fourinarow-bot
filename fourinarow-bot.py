#!/usr/bin/env python
#---------------------------------------------------------------------#
# Four In A Row AI Challenge - Starter Bot                            #
# ============                                                        #
#                                                                     #
# Last update: 30 Mar, 2016                                           #
#                                                                     #
# @author Lukas Knoepfel <shylux@gmail.com>                           #
# @version 1.0                                                        #
# @license MIT License (http://opensource.org/licenses/MIT)           #
#---------------------------------------------------------------------#
from sys import stdin, stdout, stderr
import numpy as np
import random
import time


class Bot(object):
    settings = {}
    round = -1
    board = np.zeros((6, 7), dtype=np.uint8)  # Access with [row_nr, col_nr]. [0,0] is on the top left.
    timeout = -1

    def make_turn(self):
        """ This method is for calculating and executing the next play.
            Make the play by calling place_disc exactly once.
        """
        raise NotImplementedError()

    def place_disc(self, column):
        """ Writes your next play in stdout. """
        stdout.write("place_disc %d\n" % column)
        stderr.write("place_disc %d\n" % column)
        stdout.flush()

    def simulate_place_disc(self, board, col_nr, curr_player):
        """ Returns a board state after curr_player placed a disc in col_nr.
            This is a simulation and doesn't update the actual playing board. """
        if board[0, col_nr] != 0:
            raise Bot.ColumnFullException()
        new_board = np.copy(board)
        for row_nr in reversed(range(self.rows())):
            if new_board[row_nr, col_nr] == 0:
                new_board[row_nr, col_nr] = curr_player
                return new_board

    def four_in_row(self, board, player):
        win = (self._check_horizonal(board, player) or
               self._check_vertical(board, player) or
               self._check_diagonal_up(board, player) or
               self._check_diagonal_down(board, player))
        return win

    def _check_horizonal(self, board, player):
        for row_nr in range(self.rows()):
            for col_nr in range(0, self.cols()-4):
                if board[row_nr][col_nr] == player \
                        and board[row_nr][col_nr+1] == player \
                        and board[row_nr][col_nr+2] == player \
                        and board[row_nr][col_nr+3] == player:
                            return True
        return False

    def _check_vertical(self, board, player):
        for col_nr in range(self.cols()):
            for row_nr in range(self.rows()-4):
                if board[row_nr][col_nr] == player \
                        and board[row_nr+1][col_nr] == player \
                        and board[row_nr+2][col_nr] == player \
                        and board[row_nr+3][col_nr] == player:
                            return True
        return False

    def _check_diagonal_up(self, board, player):
        for row_nr in range(0, self.rows()-4):
            for col_nr in range(0, self.cols()-4):
                if board[row_nr][col_nr] == player \
                        and board[row_nr+1][col_nr+1] == player \
                        and board[row_nr+2][col_nr+2] == player \
                        and board[row_nr+3][col_nr+3] == player:
                            return True
        return False

    def _check_diagonal_down(self, board, player):
        for row_nr in range(self.rows(), 4):
            for col_nr in range(self.cols(), 4):
                if board[row_nr][col_nr] == player \
                        and board[row_nr-1][col_nr-1] == player \
                        and board[row_nr-2][col_nr-2] == player \
                        and board[row_nr-3][col_nr-3] == player:
                            return True
        return False

    def id(self):
        """ Returns own bot id. """
        return self.settings['your_botid']

    def rows(self):
        """ Returns amount of rows. """
        return self.settings['field_rows']

    def cols(self):
        """ Returns amount of columns. """
        return self.settings['field_columns']

    def current_milli_time(self):
        """ Returns current system time in milliseconds. """
        return int(round(time.time() * 1000))

    def set_timeout(self, millis):
        """ Sets time left until timeout in milliseconds. """
        self.timeout = self.current_milli_time() + millis

    def time_left(self):
        """ Get how much time is left until a timeout. """
        return self.timeout - self.current_milli_time()

    def run(self):
        """ Main loop.
        """
        while not stdin.closed:
            try:
                rawline = stdin.readline()
                print('rawline recieved', stderr)
                # End of file check
                if not len(rawline):
                    break
                line = rawline.strip()
                # Empty lines can be ignored
                if not len(line):
                    continue
                parts = line.split()
                command = parts[0]
                self.parse_command(command, parts[1:])
            except EOFError:
                return

    def parse_command(self, command, args):
        if command == 'settings':
            key, value = args
            if key in ('timebank', 'time_per_move', 'your_botid', 'field_columns', 'field_rows'):
                value = int(value)
            self.settings[key] = value
        elif command == 'update':
            sub_command = args[1]
            args = args[2:]
            if sub_command == 'round':
                self.round = int(args[0])
            elif sub_command == 'field':
                self.parse_field(args[0])
        elif command == 'action':
            self.set_timeout(int(args[1]))
            self.make_turn()

    def parse_field(self, str_field):
        self.board = np.fromstring(str_field.replace(';', ','), sep=',', dtype=np.uint8).reshape(self.rows(), self.cols())


    class ColumnFullException(Exception):
        """ Raised when attempting to place disk in full column. """


class UltiBot(Bot):
    def make_turn(self):
        for col in range(self.cols()):
            board = self.simulate_place_disc(self.board, col, self.id())
            if self.four_in_row(board, self.id()):
                self.place_disc(col)
                return
        self.place_disc(random.randrange(7))


if __name__ == '__main__':
    """ Run the bot! """
    UltiBot().run()
