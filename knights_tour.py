import time
import logging
import multiprocessing 
#I should consider logging so I can view STDOUT and have it write to disk 

class GameError(Exception):
    def __init__(self):
        print "tour didn't work"
    
class Verbose(object):
    
    Initialized = False
    
    def __init__(self, verbosity):
        assert type(verbosity) is int, "verbose takes an integer value of 0-31"
        self.verbose_int = verbosity
        self.info = """
        bit 0[-1](1)    - max/min values
        bit 1[-2](2)    - retrace
        bit 2[-3](4)    - visited positions
        bit 3[-4](8)    - board when it changes
        bit 4[-5](16)   - every move
        bit 5[-6](32)   - recording failed position
        bit 6[-7](64)   - progress (how many moves have been made)
        bit 7[-8](128)  - potential OBOB
        bit 8[-9](256)  - possible moves
        bit 9[-10](512) - final positions
        """
        #create an 8bit string representing the verbose type mask
        self.verbose = bin(verbosity)[2:].zfill(10)

        #values for development and debugging
        self.min_max_switch = int(self.verbose[-1])
        self.retrace_switch = int(self.verbose[-2])
        self.visited_positions_switch = int(self.verbose[-3])
        self.board_switch = int(self.verbose[-4])
        self.every_move_switch = int(self.verbose[-5])
        self.failed_position_switch = int(self.verbose[-6])
        self.progress_switch = int(self.verbose[-7])
        self.potential_OBOB_switch = int(self.verbose[-8])
        self.possible_moves_switch = int(self.verbose[-9])

        #for final user to see resulting position
        self.final_positions_switch = int(self.verbose[-10])

        self._print_verbose_info()
        Verbose.Initialized = True
            
    def min_max(self, tour, largest_tour):
        #as the tour progresses, will show the longest tour, and if the tour shrinks to a small size
        new_max = False
        if len(tour.knight.visited_positions) > largest_tour:
            new_max = True
            largest_tour = len(tour.knight.visited_positions)
        if self.min_max_switch:
            if new_max:
                print "current largest tour", str(largest_tour)
            elif len(tour.knight.visited_positions) in [1,2,3]:
                print "size of the tour got pretty small with length ", str(len(tour.knight.visited_positions))
        return largest_tour
    
    def failed_position(self, old_position, failed_moves):
        if self.failed_position_switch:
            print "\told position", old_position
            for i in failed_moves:
                print "\t\t failed move", i

    def final_positions(self, chess_piece):
        if self.final_positions_switch:
            print "no solution, but here's what was tried"            
            for i in chess_piece.trials:
                print "\t", i
                for j in chess_piece.get_failed_moves(i):
                    print "\t\t", j

    def retrace(self, chess_piece):
        if self.retrace_switch:
            print "Retracing to ", chess_piece.visited_positions[-1]
        if self.visited_positions_switch:
            self.final_positions(chess_piece)

    def potential_OBOB(self, tour):
        if self.potential_OBOB_switch:
            if len(tour.knight.visited_positions) in [58,59]:
                print "possible OBOB with len", len(tour.knight.visited_positions) 
                for pos in tour.knight.visited_positions:
                    print pos

    def progress(self, count):
        if self.progress_switch:                            
            if count % 100000 == 0:
                print str(count), "moves tried so far"

    def every_move(self, move):
        if self.every_move_switch:
            print "moving to", move

    def board(self, chess_piece):
        if self.board_switch:
            board = chess_piece.get_board()
            for row in range(1, board.rows+1):
                for column in range(1, board.columns+1):
                    knight_present = False
                    fail_present = False
                    for i in chess_piece.visited_positions:
                        if row == i.row and column == i.column:
                            print chess_piece.visited_positions.index(i), "\t",
                            knight_present = True
                            break
                    if knight_present == True:
                        continue
                    for i in chess_piece.trials:
                        #must convert coordinate back into position; should be able to get rid of the if statement
                        if type(i) is tuple and len(i) == 2:
                            i = Position(row=i[0], column=i[1], board=board, verbosity=0) 
                        for j in chess_piece.get_failed_moves(i):
                            if row == j.row and column == j.column:
                                print "F\t",
                                fail_present = True
                                break
                        if fail_present == True:
                            break
                    if knight_present == False and fail_present == False:
                        print "x\t",
                print "\n"
            raw_input("press any key to continue")

    def possible_moves(self, origin, moves):
        if self.possible_moves_switch:
            print "possible moves from position", origin
            for move in moves:
                print "\t", move
                
    def _print_verbose_info(self):
        if self.verbose_int > 0 and self.verbose_int != 512 and Verbose.Initialized == False:
            print self.info
            print "current verbose settings...\n"
            for i in dir(self):
                value = getattr(self, i)
                if "switch" in str(i):
                    spacing = "\t"
                    for j in range(3-(len(i)/8)):
                        spacing += "\t"
                    print i, spacing, getattr(self, i)
            print "\n"

class Board(object):

    def __init__(self, rows, columns, verbosity):
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = self.rows * self.columns
        #calculate how many moves a position is away from the edge of the board then add 1
        #should be represented as a relationship between possible moves and how close it is to the edge of the board
        #due to the weights, this is sort of solely a knight tour problem
        self.moves = {2:2, 3:3, 4:4, 5:6, 6:8} #shows how many moves are possible given how close the position is to the edge of the board
        self.verbosity = Verbose(verbosity)

    def get_weight(self, row, column):
        #for now, if a chess piece is 3 deep, it's weighted the same as all other inner pieces, hence limiting the depth to a max of 3
        row_depth = min(row, self.rows-row+1, 3)
        column_depth = min(column, self.columns-column+1, 3)
        return self.moves.get(column_depth + row_depth, None)
        
# a move eg. (1,2), (-2,1) should maybe have it's own class?

class Position(object):

    def __init__(self, row, column, board, verbosity):
        self.row = row
        self.column = column
        self.coordinate = (row, column)
        self.board = board
        self.verbosity = Verbose(verbosity)
        self.fits_on_board = self._check_board()
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
        #return "Row:", self.row, " Column:", self.column 
    
    def _check_board(self):
        if not 0 < self.row <= self.board.rows:
                return False
        if not 0 < self.column <= self.board.columns:
                return False
        return True
    
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
        #self.record_failed_position(self.current_position, position)
        self.current_position = position
        self.verbosity.board(self)
        return added
        
    def record_failed_position(self, old_position, new_position):
        failed_moves = self.get_failed_moves(old_position)
        self.verbosity.failed_position(old_position, failed_moves)
        failed_moves.add(new_position)
        self.trials[old_position.coordinate] = failed_moves

    def retrace(self):
        
        failed_position = self.visited_positions.pop()
        try:
            previous_position = self.visited_positions[-1]
        except:
            self.verbosity.final_positions(self)
            raise GameError()
            
        self.record_failed_position(previous_position, failed_position) #this might not be necissary as this should have already been recorded, or I only use this, and get rid of setting failed positions when I move the knight in the first place to be a little less confusing
#        failed_positions = self.get_failed_moves(previous_position)
#        failed_positions.add(failed_position)
        self.set_position(previous_position)
        self.verbosity.retrace(self)
        #should remove failed positions recursively from failed_position
        print "removing failed position for", previous_position
        self.remove_failed_positions(previous_position.coordinate)
        return previous_position

    def remove_failed_positions(self, failed_position):
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


        print "current failed positions for ", position 
        for i in failed_positions:
            print i


        
        for i in failed_positions:
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
            

class Tour(object):

    def __init__(self, rows, columns, start_position, verbosity=0):
        self.verbosity = Verbose(verbosity)
        self.board = Board(rows, columns, self.verbosity.verbose_int)
        self.start_position = self._generate_start_position(start_position)
        self.retrace = 0 #just in case I want to set up a retrace counter
        

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

    def run(self):
        previous_move = self.start_position #or None
        self.knight = Knight(self.start_position, self.verbosity.verbose_int)
        count = 0
        largest_tour = 0
        while len(self.knight.visited_positions) < self.board.size:
            largest_tour = self.verbosity.min_max(self, largest_tour)
            self.verbosity.potential_OBOB(self)
            self.verbosity.progress(count)
            print "previous move", previous_move                
            possible_moves = self.knight.get_possible_moves(previous_move)
            self.verbosity.possible_moves(self.knight.get_current_position(), possible_moves)
            if len(possible_moves) == 0:
                previous_move = self._end_of_game(possible_moves)
                if type(previous_move) == type(self.knight.current_position):
                    count += 1
                    continue
                elif self._end_of_game(possible_moves) == "Finished":
                    return self.knight.visited_positions
            else:
                move_combos = self._create_second_moves(possible_moves)
                if len(move_combos) == 0:
                    print "move combos len is 0"
                    if self.knight.set_position(self.knight.current_position) == True:
                        if self._end_of_game(move_combos):
                            return self.knight.visited_positions
                        else:
                            pass #not sure what to do here
                    else:
                        previous_move = self.knight.retrace()
                        self._check_tour(previous_move)
                        count += 1
                        continue
                else:
                    previous_move = self._choose_best_move(move_combos)
            count += 1

    def _end_of_game(self, possible_moves):
        if len(possible_moves) == 0 and len(self.knight.visited_positions) == self.board.size:
            return "Finished" 
        else:
            return self.knight.retrace()
        

    #untested
    def _create_second_moves(self, possible_moves):
        move_combos = [] #this will hold all 2 move combinations to be selected by the knight by weight
        for i in possible_moves:
            move = (i,) #each of these will hold a 2 move combination
            trial_knight1 = Knight(i, self.verbosity.verbose_int)
            trial_knight1.visited_positions = self.knight.visited_positions[:]
            k1_possible_moves = trial_knight1.get_possible_moves(self.knight.get_current_position())
            if len(k1_possible_moves) == 0:
                previous_move = self._end_of_game(possible_moves)
                if type(previous_move) == type(self.knight.current_position):
                    continue
                elif self._end_of_game(possible_moves) == "Finished":
                    return self.knight.visited_positions
            self.verbosity.possible_moves(i, k1_possible_moves)    
            for j in k1_possible_moves:
                moves = move + (j,)   
            move_combos.append(moves)
        return move_combos

    #untested
    def _choose_best_move(self, move_combos):
        good_moves = self._get_weights(move_combos)
        self.verbosity.possible_moves(self.knight.get_current_position(), good_moves)
        for move in good_moves:
            self.knight.set_position(move)
            
        previous_move = good_moves[0]

        if good_moves[1] in self.knight.get_failed_moves(previous_move):
            previous_move = self.knight.retrace()
        """
        else:
            self.knight.set_position(good_moves[1])
        """

        self.knight.record_failed_position(previous_move, good_moves[1])
        return previous_move        

    def _check_if_finished(self, possible_moves):
        previous_move = None
        if len(possible_moves) == 0:
            if len(self.knight.visited_positions) < self.board.size:
                previous_move = self.knight.retrace() #or do last move here visited_positions[-1]
                self._check_tour(previous_move)
            else:
                self.knight.set_position(previous_move)
                return "Finished"
        return previous_move

    def _check_tour(self, previous_move):
        if previous_move == self.start_position:
            print "no solution found"
                    

    def _get_weights(self, move_combos):
        #two positions will be returned that have a weight less than or equal to other possible position combinations
        #the tour will use those two positions with the minimum weight to move the knight
        weights = {}
        for i in move_combos:
            weight = i[0].weight + i[1].weight
            weights[weight] = i   
        return weights.get(min(weights),None) #maybe i want max here but I doubt it

def main(rows=3, columns=3, starting_location="2.3", verbosity=1023): #was 907
    start_time = time.time()
    if None in [rows, columns, starting_location, verbosity]:
        print "\tEnter 'e' or 'exit' to skip the prompts and exit the program...\n"
    if rows == None:
        rows = raw_input("how many rows would you like on the chess board?\n")
        if rows.lower() == "e" or rows.lower() == "exit":
            return
    if columns == None:
        columns = raw_input("How many columns would you like on the chess board?\n")
        if columns.lower() == "e" or columns.lower() == "exit":
            return
    if starting_location == None:
        starting_location = raw_input("which coordinate which you like to be the starting location?  (please enter in the format of row.column, eg. 4.5)\n")
        if starting_location.lower() == "e" or starting_location.lower() == "exit":
            return
    if verbosity == None:
        verbosity = raw_input("would you like to display the ordered coordinates for the final tour? (y/n)\n")
        if verbosity.lower() == "y" or verbosity.lower() == "yes":
            verbosity = 512
        else:
            verbosity = 0
    t = Tour(rows, columns, starting_location, verbosity)
    try:
        result = t.run()
        #run multiple instances of the tour, and the one with the smallest difference between
        #their biggest tour and rebound down to smallest  visited positions.
        #big rebounds means a lot of possiblilities were ruled out
    except GameError:
        print "took", time.time() - start_time
        return
    for i in result:
        print i
        print "took", time.time() - start_time
    
#"""
if __name__ == "__main__":
    print "Welcome to Knights Tour!\n"
    main()
#"""

def test_data(rows=3, columns=3, row=2, column=6, start="4.5"):
    tour = Tour(rows, columns, start, verbosity=0)
    board = Board(rows, columns, tour.verbosity.verbose_int)
    position = Position(row, column, board, tour.verbosity.verbose_int)
    knight = Knight(position, tour.verbosity.verbose_int)
    return tour, board, position, knight

