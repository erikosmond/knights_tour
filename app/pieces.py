from app.verbose import Verbose

class GameError(Exception):
    def __init__(self):
        print "tour didn't work"

class ChessPiece(object):

    knight_moves = None
        
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
        return self.current_position

    def get_board(self):
        return self.current_position.board
        
    def get_failed_moves(self, position):
        if type(position) is tuple:
            return self.trials.get(position, set()) #this is potentially sloppy code that I should fix
        return self.trials.get(position.coordinate, set())

    def record_visited_position(self, position):
        if position not in self.visited_positions:
            self.visited_positions.append(position)
            return True

    def set_position(self, position):
        self.verbosity.every_move(position)
        added = self.record_visited_position(position)
        #self.record_failed_position(self.current_position, position) #this was commented out, it duplicates in knight.retrace()
        self.current_position = position
        self.verbosity.board(self)
        return added



    ###modify this method to adjust the position instead
    def record_failed_position(self, old_position, new_position):
        old_position.record_failed_position(new_position)
        #self.verbosity.failed_position(old_position, failed_moves) #This needs to be changed to reflect the trials being in the position
        """
        failed_moves = self.get_failed_moves(old_position)
        failed_moves.add(new_position)
        self.trials[old_position.coordinate] = failed_moves
        """
    def retrace(self):  ##create retrace objects so I don't have to manage the memory:)
        """
        A knight can inherit both a chess_piece and a retrace, or should I have them all be conneted via inheritence?
        I need to rethink the way i'm doing retraces because this two steps forward one step back thing is
        really confusing, and I'm not incorporating
        the fact that that is happening enough into my thinking
        It might explain why it was easy to go back one step, but not two steps and why the failed positions seemed to grow and weird times
        a move should be its own object and a retrace should inherit it
        """
        #pre retrace - print current possition, all possible moves from that position, and all failed moves on the board
        failed_position = self.visited_positions.pop()
        try:
            previous_position = self.visited_positions[-1]
        except:
            self.verbosity.final_positions(self)
            raise GameError()
        self.set_position(previous_position)
        self.verbosity.retrace(self)
        print "removing failed position for", previous_position
        self.remove_failed_positions(previous_position.coordinate)
        self.record_failed_position(previous_position, failed_position) #this might not be necissary as this should have already been recorded, or I only use this, and get rid of setting failed positions when I move the knight in the first place to be a little less confusing
        #post retrace - print current position, the failed position, all possible moves from the current position and all stored failed moves

        return previous_position

    def remove_failed_positions(self, failed_position): #now that failed trials are held in the position, I should be able to get rid of this
        failed_positions = self.get_failed_moves(failed_position)
        print str(failed_positions), "are the failed positions for", str(failed_position)
        if failed_positions == set():
            return
        else:
            for i in failed_positions:
                self.remove_failed_positions(i.coordinate)
        self.trials[failed_position] = set()
    
    def reset_possible_positions(self): #I should be able to remove this; do a quick find to be sure
        self.possible_positions = [ ]

    #passing previous one into this method should eliminate need for self.possible_positions    
    def get_possible_moves(self, previous_move):
        possible_moves = [ ] 
        for i in self.moves:
            possible_position = self.current_position.get_new_position(i[0], i[1])
            if self._valid_position(possible_position) and not possible_position == previous_move:
                possible_moves.append(possible_position)
        return possible_moves       
        
    def _valid_position(self, position):
        #print position, "Fits on board:", str(position.fits_on_board)
        if not position.fits_on_board:
            return False
        #depending on how many moves in advance I go, I might not need this for loop below, I'll still need the visited positions for loop though
        failed_positions = self.get_failed_moves(self.get_current_position())


        print "current failed positions for in _valid_position method", position 
        for i in failed_positions:
            print i

        if self.current_position.check_failed_position(position) == True:
            #if it's already a failed position, return False
            return False
        
        for i in failed_positions: #should be able to remove this check with code above
            if position == i:
                return False

            
        for i in self.visited_positions:
            if position == i:
                return False        
        return True 
        
class Knight(ChessPiece):

    legal_moves = ((1,2),(2,1))

    def __init__(self, position, verbosity):
        self.current_position = position
        self.visited_positions = [self.current_position]
        self.possible_positions = [ ]
        if ChessPiece.knight_moves == None:
            ChessPiece.knight_moves = self.create_moves()
        self.moves = ChessPiece.knight_moves
        self.verbosity = Verbose(verbosity)
        self.trials = {}#coordinate: [failed_coordinate1, failed_coordinate2]