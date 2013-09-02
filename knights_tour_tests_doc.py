#import doctest
from knights_tour import Board, Position, ChessPiece, Knight, Tour

#I could potentially have one function that calls all other fuctions, so I can create one board and just pass that into each test

def get_weight_from_board(rows, columns, row, column):
    """
    The first test expects to have None returned, thus the empty space
    >>> get_weight_from_board(rows=0, columns=0, row=0, column=0)

    This test would be None but should not happen as only positions that fit on a board should get a weight
    >>> get_weight_from_board(rows=4, columns=4, row=5, column=3)
    2

    >>> get_weight_from_board(rows=8, columns=8, row=8, column=8)
    2
    >>> get_weight_from_board(rows=8, columns=8, row=8, column=1)
    2
    >>> get_weight_from_board(rows=8, columns=8, row=4, column=5)
    8
    
    >>> get_weight_from_board(rows=4, columns=4, row=2, column=1)
    3
    
    """
    board = Board(rows, columns)
    return board.get_weight(row, column)

def knight_moves(rows, columns, row1, column1, row2, column2):
    """
    Tests to see if a second knight is created, it has the proper knight moves
    >>> knight_moves(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    True

    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight1 = Knight(position1)
    knight2 = Knight(position2)
    return knight1.moves == knight2.moves

def position_fits_on_board(rows, columns, row, column):
    """
    >>> position_fits_on_board(rows = 8, columns = 8, row = 4, column = 5)
    True
    >>> position_fits_on_board(rows = 4, columns = 4, row = 5, column = 3)
    False
    >>> position_fits_on_board(rows = 8, columns = 8, row = 9, column = 8)
    False
    >>> position_fits_on_board(rows = 0, columns = 0, row = 9, column = 8)
    False
    >>> position_fits_on_board(rows = 8, columns = 8, row = 8, column = 8)
    True
    >>> position_fits_on_board(rows = 8, columns = 8, row = 1, column = 1)
    True
    """
    board = Board(rows, columns)
    return Position(row, column, board).fits_on_board

def get_new_position(rows, columns, row, column, rdelta, cdelta):
    """
    >>> get_new_position(rows=8, columns=8, row=8, column=8, rdelta=-1, cdelta=-2)
    (7, 6)
    >>> get_new_position(rows=8, columns=8, row=8, column=8, rdelta=1, cdelta=2)
    (9, 10)
    
    """
    board = Board(rows, columns)
    position = Position(row, column, board)
    new_position = position.get_new_position(rdelta, cdelta)
    return (new_position.row, new_position.column)

def equal_position(rows, columns, row1, column1, row2, column2):
    """
    >>> equal_position(rows=8, columns=8, row1=8, column1=8, row2=8, column2=8)
    True
    >>> equal_position(rows=8, columns=8, row1=8, column1=11, row2=8, column2=11)
    True
    >>> equal_position(rows=8, columns=8, row1=8, column1=8, row2=8, column2=0)
    False
    >>> equal_position(rows=8, columns=8, row1=4, column1=8, row2=8, column2=4)
    False
    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)    
    position2 = Position(row2, column2, board)
    return position1 == position2

def check_board(rows, columns, row, column):
    """
    >>> check_board(rows = 8, columns = 8, row = 9, column = 8)
    False
    >>> check_board(rows = 8, columns = 8, row = 5, column = 5)
    True
    >>> check_board(rows = 8, columns = 8, row = 0, column = 5)
    False
    >>> check_board(rows = 8, columns = 8, row = 8, column = 8)
    True
    """
    board = Board(rows, columns)
    position = Position(row, column, board)
    return position._check_board()

def valid_pieces(rows=8, columns=8, row=9, column=8):
    board = Board(rows, columns)
    position = Position(row, column, board)
    print position.fits_on_board
    

def valid_possible_position1(rows, columns, row1, column1, row2, column2):
    """
    >>> valid_possible_position1(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    False

    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight = Knight(position1)
    knight.record_visited_position(position2)
    return knight._valid_position(position1)

def valid_possible_position2(rows, columns, row1, column1, row2, column2):
    """
    >>> valid_possible_position2(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    False

    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight = Knight(position1)
    knight.record_visited_position(position2)
    return knight._valid_position(position2)

def valid_possible_position3(rows, columns, row1, column1, row2, column2):
    """
    >>> valid_possible_position3(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    True
    >>> valid_possible_position3(rows=8, columns=8, row1=4, column1=5, row2=5, column2=11)
    False
    >>> valid_possible_position3(rows=8, columns=8, row1=9, column1=9, row2=5, column2=7)
    True
    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight = Knight(position1)
    return knight._valid_position(position2)

def get_possible_moves(rows, columns, row, column):
    """
    >>> get_possible_moves(rows = 8, columns = 8, row = 8, column = 8)
    [(7, 6), (6, 7)]
    >>> get_possible_moves(rows = 8, columns = 8, row = 4, column = 5)
    [(5, 7), (5, 3), (3, 7), (3, 3), (6, 6), (6, 4), (2, 6), (2, 4)]
    """
    board = Board(rows, columns)
    position = Position(row, column, board)
    knight = Knight(position)
    positions = []
    for p in knight.get_possible_moves(position):
        positions.append(p.coordinate)
    return positions

def get_possible_moves2(rows, columns, row1, column1, row2, column2):
    """
    >>> get_possible_moves2(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    [(5, 3), (3, 7), (3, 3), (6, 6), (6, 4), (2, 6), (2, 4)]

    (5, 7) should not appear

    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight = Knight(position1)
    positions = []
    for p in knight.get_possible_moves(position2):
        positions.append(p.coordinate)
    return positions

def create_moves(rows, columns, row, column):
    """
    Test creating all knight moves
    
    >>> create_moves(rows = 8, columns = 8, row = 8, column = 8)
    ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
    """
    board = Board(rows, columns)
    position = Position(row, column, board)
    knight = Knight(position)
    return knight.create_moves()

def record_visited_position(rows, columns, row1, column1, row2, column2):
    """
    >>> record_visited_position(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    [(4, 5), (5, 7)]

    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight = Knight(position1)
    knight.record_visited_position(position2)
    positions = []
    for pos in knight.visited_positions:
        positions.append(pos.coordinate)
    return positions

def retrace_pop(rows, columns, row1, column1, row2, column2):
    """
    >>> retrace_pop(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    (5, 7)

    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight = Knight(position1)
    knight.record_visited_position(position2)
    return knight.retrace().coordinate

def retrace_visited(rows, columns, row1, column1, row2, column2):
    """
    >>> retrace_visited(rows=8, columns=8, row1=4, column1=5, row2=5, column2=7)
    (4, 5)

    """
    board = Board(rows, columns)
    position1 = Position(row1, column1, board)
    position2 = Position(row2, column2, board)
    knight = Knight(position1)
    knight.record_visited_position(position2)
    knight.retrace()
    return knight.visited_positions[0].coordinate

def generate_start_position(rows, columns, position_coordinate):
    """
    Test Tour._generate_start_position
    
    >>> generate_start_position(rows=8, columns=8, position_coordinate="4.5")
    (4, 5)

    """
    tour = Tour(rows, columns, position_coordinate)
    position = tour._generate_start_position(position_coordinate)
    return position.coordinate

def get_weights_from_tour(rows, columns, position_coordinate, row1, column1, row2, column2):
    """
    Test Tour._get_weights
    
    >>> get_weights_from_tour(rows=8, columns=8, position_coordinate="4.5",row1=8, column1=8, row2=5, column2=4)
    10

    """
    tour = Tour(rows, columns, position_coordinate)
    position1 = Position(row1, column1, tour.board)
    position2 = Position(row2, column2, tour.board)
    position3 = Position(row1-1, column1-1, tour.board)
    position4 = Position(row2-1, column2-1, tour.board)
    position_tuple = tour._get_weights([(position1, position2),(position3,position4)])
    return position_tuple[0].weight + position_tuple[1].weight


"""

class Tour(object):

    def __init__(self, rows, columns, start_position, verbose=True):
        self.board = Board(rows, columns)
        self.start_position = self._generate_start_position(start_position)
        self.retrace = 0 #just in case I want to set up a retrace counter
        self.verbose = verbose
        #self.trials = {}#coordinate: [failed_coordinate1, failed_coordinate2]

    def tour(self):
        previous_move = None
        knight = Knight(self.start_position)
        while len(knight.visited_positions) < self.board.size:
            #return moves that will keep the knight on the board and not backtrack
            possible_moves = knight.get_possible_moves(previous_move)
            end = self._check_moves(possible_moves)
            if end:
                return knight.visited_positions
            move_combos = [] #this will hold all 2 move combinations to be selected by the knight by weight
            for i in possible_moves:
                moves = () #each of these will hold a 2 move combination
                position = knight.current_position.get_new_position(i.row, i.column)
                moves = moves + (position,)
                trial_knight1 = Knight(position)                
                k1_possible_moves = trial_knight1.get_possible_moves(position)
                for j in k1_possible_moves:
                    position1 = trial_knight1.current_position.get_new_position(j.row, j.column)
                    trial_knight1.set_position(position1)
                    moves = moves + (position,)
                    move_combos.append(moves)
            good_moves = self._get_weights(move_combos)
            for move in good_moves:
                knight.record_visited_position(move)
            knight.set_position(good_moves[1])    
                

    def _check_moves(self, possible_moves):
        if len(possible_moves) == 0:
            if len(knight.visited_positions) < board.size:
                previous_move = knight.retrace()
                self._check_tour(previous_move)
            else:
                return True

    def _check_tour(self, previous_move):
        if previous_move == self.start_position:
            print "no solution found"
            exit(2)        

    def _get_weights(self, move_combos):
        weights = {}
        for i in move_combos:
            print i[0], i[1]
            weight = i[0].weight + i[1].weight
            weights[weight] = i
        return weights[min(weights)] #maybe i want max here but I doubt it   
    
"""
if __name__ == '__main__':
    import doctest
    #doctest will only return anything only if there is a failure
    doctest.testmod()                                         
