from app.verbose import Verbose

class Board(object):

    def __init__(self, rows, columns, verbosity=0):
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = self.rows * self.columns
        #for both row and column, calculate how many moves a position is away from the edge of the board then add 1 
        self.moves = {2:2, 3:3, 4:4, 5:6, 6:8} #shows how many moves are possible given how close the position is to the edge of the board
        self.verbosity = Verbose(verbosity)

    def get_weight(self, row, column):
        #for now, if a chess piece is 3 deep, it's weighted the same as all other inner pieces, hence limiting the depth to a max of 3
        row_depth = min(row, self.rows-row+1, 3)
        column_depth = min(column, self.columns-column+1, 3)
        return self.moves.get(column_depth + row_depth, None)

class Position(object):

    def __init__(self, row, column, board, verbosity=0):
        self.row = row
        self.column = column
        self.coordinate = (row, column)
        self.board = board
        self.verbosity = Verbose(verbosity)
        self.fits_on_board = self._check_board()
        self.failures = []
        self.retrace = False
        if self.fits_on_board:
            self.weight = self.board.get_weight(self.row, self.column)
        else:
            self.weight = None
            
    def get_new_position(self, row_delta, column_delta):
        new_row = self.row + row_delta
        new_column = self.column + column_delta
        return Position(new_row, new_column, self.board, self.verbosity.verbose_int)
        
    def __eq__(self, other):
        return self.coordinate == other.coordinate #could additionally check to see if the positions are on the same board

    def __str__(self):
        return "Row: %s, Column: %s" %(self.row, self.column)
    
    def _check_board(self):
        if not 0 < self.row <= self.board.rows:
                return False
        if not 0 < self.column <= self.board.columns:
                return False
        return True

    def record_failed_position(self, position):
        self.failures.append(position)
        
    def get_weight(self):
        return self.weight
    
    def set_retrace(self):
        self.retrace = True
    
    def check_failed_position(self, position):
        if position in self.failures:
            return True
        return False