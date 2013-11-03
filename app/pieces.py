from verbose import Verbose
from board import Position

class GameError(Exception):
    def __init__(self):
        print "No solutions found\n"

class ChessPiece(object):

    knight_moves = None #This ensures I only calculate legal knight moves once
    debug_position = (13, 13)# (6, 4)
        
    def create_moves(self):
        all_moves = tuple()
        for i in self.legal_moves:
            moves = self._combine_moves(i)
            all_moves = all_moves + moves
        return all_moves    
    
    def _combine_moves(self, move):
        #for each legal move, this will create each variation of that move on a 2D board
        move1 = (move[0], move[1])
        move2 = (move[0], -move[1])
        move3 = (-move[0], move[1])
        move4 = (-move[0], -move[1])        
        return (move1, move2, move3, move4)
        
    def get_current_position(self):
        return self.visited_positions[-1]

    def get_board(self):
        return self.get_current_position().board

    def record_visited_position(self, position, retrace=False):
        #this is a duplicate check as it should have been handled in self._valid_position
        if position not in self.visited_positions:
            self.visited_positions.append(position)
            return True
        elif retrace == True:
            self.get_current_position().set_retrace()

    def get_visited_positions(self):
        return self.visited_positions
    
    def set_position(self, position, retrace=False):
        if retrace == True:
            position.set_retrace()
        self.verbosity.every_move(position)
        added = self.record_visited_position(position, retrace)
        if len(self.visited_positions) == self.get_board().size - 1:
            self.verbosity.board(self)
        return added

    def record_failed_position(self, old_position, new_position):
        old_position.record_failed_position(new_position)
        
        #This needs to be changed to reflect the trials being in the position        
        #self.verbosity.failed_position(old_position, failed_moves) 
        
    def retrace(self):
        failed_position = self.visited_positions.pop()
        #print self.visited_positions
        try:
            previous_position = self.visited_positions[-1]
        except:
            print "retrace exception"
            self.verbosity.final_positions(self)
            raise GameError()
        self.set_position(previous_position, retrace=True)
        self.verbosity.retrace(self)
        self.record_failed_position(previous_position, failed_position)

        return previous_position

    def get_possible_moves(self):
        possible_moves = [ ]
        for i in self.all_possible_moves[self.get_current_position().coordinate]:
            if self._valid_position(i):
                #when these positions are reused, they should have no memory of previous failed positions as they already had to be retraced
                i.reset_failures() 
                possible_moves.append(i)
        return possible_moves       
        
    def _valid_position(self, position):
        if position.fits_on_board != True: #should be able to remove this check
            return False
        
        if self.get_current_position().check_failed_position(position) == True:
            #if it's already a failed position, return False
            #debug info
            if self.get_current_position().coordinate == self.debug_position:
                print "failed position", position
            return False
            
        for i in self.visited_positions:
            if position == i:
                #debug info
                if self.get_current_position().coordinate == self.debug_position:
                    print "visited position", i
                return False  
        return True 
        
class Knight(ChessPiece):

    legal_moves = ((1,2),(2,1))

    def __init__(self, position, verbosity=0):
        #self.current_position = position
        self.visited_positions = [position]
        self.possible_positions = [ ]
        if ChessPiece.knight_moves == None:
            ChessPiece.knight_moves = self.create_moves()
        self.moves = ChessPiece.knight_moves
        self.verbosity = Verbose(verbosity)
        
    def get_tour(self): #this should be moved to parent class
        final_tour = []
        for position in self.get_visited_positions():
            info = str(position.row) + '.' + str(position.column) 
            if position.retrace == True:
                info = info + '.' + "retrace"
            else:
                info = info + '.' + "progress" 
            final_tour.append(info)
        return final_tour
    
    def add_to_board(self, board):
        moves = {}
        for row in range(1, board.rows+1):
            for column in range(1, board.columns+1):
                p = Position(row, column, board, self.verbosity.verbose_int)
                possible_positions = []
                for i in self.moves:
                    possible_position = p.get_new_position(i[0], i[1])
                    if possible_position.fits_on_board:
                        possible_positions.append(possible_position)
                moves[p.coordinate] = possible_positions
        Knight.all_possible_moves = moves
        
    
    #for every position on the board, I want to know all the knights possible moves from that position
    #add knight to board - knight.add_to_board(board)
    # moves = {}
    # for row in board.rows
    #   for column in board.columns
    #       p = Position(row, column, board, self.verbosity)
    #       possible_positions = []
    #       for i in self.moves:
    #           possible_position = p.get_new_position(i[0], i[1])
    #           if position.fits_on_board:
    #              possible_positions.append(possible_position)
    #       moves[p.coordinate] = possible_positions
    # self.possible_moves = moves
    
    #{'1.1':['2.3', '3.2']}