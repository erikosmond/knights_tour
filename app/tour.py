from app.board import Board, Position
from app.pieces import Knight
from app.verbose import Verbose
from app.move import Move
from app.trace import Trace

class MoveError(Exception):
    
    def __init__(self, position):
        print "Knight can not move to", position, " as it has already been visited."
    


class Tour(object):

    def __init__(self, rows, columns, start_position, verbosity=0, closed=False):
        self.verbosity = Verbose(verbosity)
        self.closed = closed
        self.board = Board(rows, columns, self.verbosity.verbose_int)
        self.start_position = self._generate_start_position(start_position)
        self.retrace = 0 #just in case I want to set up a retrace counter
        self.end_positions = None
        
    def run(self):
        self.knight = Knight(self.start_position, self.verbosity.verbose_int)
        if self.closed == True:
            self.end_positions = self.knight.get_possible_moves()
        count = 0
        largest_tour = 0
        while len(self.knight.visited_positions) < self.board.size:
            #garner stats
            largest_tour = self.verbosity.min_max(self, largest_tour)
            self.verbosity.potential_OBOB(self)
            self.verbosity.progress(count)
            if len(self.knight.visited_positions) < 4:
                largest_tour = len(self.knight.visited_positions)
            
            #find the next move
            possible_positions = self.knight.get_possible_moves()
            self.verbosity.possible_moves(self.knight.get_current_position(), possible_positions)
            if len(possible_positions) == 0:
                    previous_position = self.knight.retrace()
                    t = Trace(count, previous_position, retrace=True)
                    count += 1
                    continue  
            initial_moves = []
            for position in possible_positions: #the position already has a weight when it's created
                if self._check_closed_tour(position, count) == True:
                    break
                move = Move(position, self.knight.get_visited_positions()[:])
                initial_moves.append(move)
            if len(initial_moves) != 0:
                best_move = Move.choose_best_move(initial_moves, self.end_positions)
                if not self.knight.set_position(best_move.get_position()):
                    raise MoveError(best_move.get_position())
                t = Trace(count, best_move.get_position(), retrace=False)
            count += 1
        return self.knight, count
    
    def _check_closed_tour(self, position, count):
        if len(self.knight.visited_positions) == (self.board.size -1) and self.closed == True:
            if position in self.end_positions:
                t = Trace(count, position, retrace=False)
                self.knight.set_position(position)
            else:
                previous_position = self.knight.retrace()
                t = Trace(count, previous_position, retrace=True)
            return True
    
    def _generate_start_position(self, start_position):
        error1 = "The %s value of your start position must be an integer.  Please enter the starting location in the following format: 4.5"
        error2 = "the %s (the %s value from the starting position does not fit on the board"
        row_column = start_position.split(".")      
        assert len(row_column) is 2, "start position must contain exactly one '.' period"
        try:
            row = int(row_column[0])
        except ValueError:
            print error1 %("first")
            exit(1)
        try:
            column = int(row_column[1])
        except ValueError:
            print error1 %("second")
            exit(1)
            
        assert 0 < row <= self.board.rows, error2 %("row","first")             
        assert 0 < column <= self.board.columns, error2 %("column","second")       
        return Position(row, column, self.board, self.verbosity.verbose_int)
