from app.verbose import Verbose

class GameError(Exception):
    def __init__(self):
        print "Tour didn't work"

class ChessPiece(object):

    knight_moves = None #This ensures I only calculate legal knight moves once
        
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

    def record_visited_position(self, position):
        #this is a duplicate check as it should have been handled in self._valid_position
        if position not in self.visited_positions:
            self.visited_positions.append(position)
            return True

    def get_visited_positions(self):
        return self.visited_positions
    
    def set_position(self, position, retrace=False):
        if retrace == True:
            position.set_retrace()
        self.verbosity.every_move(position)
        added = self.record_visited_position(position)
        if len(self.visited_positions) == self.get_board().size - 1:
            self.verbosity.board(self)
        return added

    def record_failed_position(self, old_position, new_position):
        old_position.record_failed_position(new_position)
        
        #This needs to be changed to reflect the trials being in the position        
        #self.verbosity.failed_position(old_position, failed_moves) 
        
    def retrace(self):
        failed_position = self.visited_positions.pop()
        try:
            previous_position = self.visited_positions[-1]
        except:
            self.verbosity.final_positions(self)
            raise GameError()
        self.set_position(previous_position, retrace=True)
        self.verbosity.retrace(self)
        self.record_failed_position(previous_position, failed_position)

        return previous_position

    def get_possible_moves(self): 
        possible_moves = [ ] 
        for i in self.moves:
            possible_position = self.get_current_position().get_new_position(i[0], i[1])
            if self._valid_position(possible_position):
                possible_moves.append(possible_position)
        return possible_moves       
        
    def _valid_position(self, position):
        if position.fits_on_board != True:
            return False
        
        if self.get_current_position().check_failed_position(position) == True:
            #if it's already a failed position, return False
            return False
            
        for i in self.visited_positions:
            if position == i:
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