class Board(object):

    def __init__(self, rows, columns):
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = self.rows * self.columns
        #calculate how many moves a position is away from the edge of the board then add 1
        #should be represented as a relationship between possible moves and how close it is to the edge of the board
        #due to the weights, this is sort of solely a knight tour problem
        self.moves = {2:2, 3:3, 4:4, 5:6, 6:8} #shows how many moves are possible given how close the position is to the edge of the board

    def get_weight(self, row, column):
        #for now, if a chess piece is 3 deep, it's weighted the same as all other inner pieces, hence limiting the depth to a max of 3
        row_depth = min(row, self.rows-row+1, 3)
        column_depth = min(column, self.columns-column+1, 3)
        return self.moves.get(column_depth + row_depth, None)
        
# a move eg. (1,2), (-2,1) should maybe have it's own class?

class Position(object):

    def __init__(self, row, column, board):
        self.row = row
        self.column = column
        self.coordinate = (row, column)
        self.board = board
        self.fits_on_board = self._check_board()
        if self.fits_on_board:
            self.weight = self.board.get_weight(self.row, self.column)
        else:
            self.weight = None
            
    def get_new_position(self, row_delta, column_delta):
        new_row = self.row + row_delta
        new_column = self.column + column_delta
        #new_position = Position(new_row, new_column, self.board)
        return Position(new_row, new_column, self.board) #or return new_position
        
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
    
#just as a test, have position inherit board and see what happens when
    #create a position with no board, see what happens when i call board attributes
    #create a board instance, then see what happens on position attrs
        #then create a position2 instance
    #create a board2 instance, see what happens for position and position2
        #create postion 3 and see what happens
    #python inheret instance vs class

#use ipython to figure out if i can make a position an instance of a board instance, not the class
    
class ChessPiece(object):

    knight_moves = None

        #I will probably remove this method given that the knight has a position and the position has a board
    def add_to_board(self, board): 
        self.board = board
        
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
        
    def set_position(self, position):
        self.current_position = position
        
    def record_visited_position(self, position):
        self.visited_positions.append(position)
        
    def retrace(self):
        
        failed_position = self.visited_positions.pop()
        previous_position = self.visited_positions[-1]
        failed_positions = self.trials.get(previous_position, set())
        failed_positions.add(failed_position)
        self.set_position(previous_position)
        print "Retracing to ", self.visited_positions[-1]
        """
        for i in self.trials:
            print "\t", i
            for j in self.trials.get(i,[]):
                print "\t\t", j
        """
        return previous_position
    
    def reset_possible_positions(self):
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
        failed_positions = self.trials.get(self.get_current_position(),set())
        for i in failed_positions:
            if position == i:
                return False
        for i in self.visited_positions:
            if position == i:
                return False        
        return True 
        
class Knight(ChessPiece):

    legal_moves = ((1,2),(2,1))

    def __init__(self, position):
        self.current_position = position
        self.visited_positions = [self.current_position]
        self.possible_positions = [ ]
        if ChessPiece.knight_moves == None:
            ChessPiece.knight_moves = self.create_moves()
        self.moves = ChessPiece.knight_moves
        self.trials = {}#coordinate: [failed_coordinate1, failed_coordinate2]
            

class Tour(object):

    def __init__(self, rows, columns, start_position, verbose=True):
        self.board = Board(rows, columns)
        self.start_position = self._generate_start_position(start_position)
        self.retrace = 0 #just in case I want to set up a retrace counter
        self.verbose = verbose

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
        return Position(row, column, self.board)

    def start_tour(self):
        previous_move = self.start_position #or None
        self.knight = Knight(self.start_position)
        while len(self.knight.visited_positions) < self.board.size:
            """
            for i in knight.visited_positions:
                print "\t\t", i
            """
            #return moves that will keep the knight on the board and not backtrack
            possible_moves = self.knight.get_possible_moves(previous_move)
            #if no moves are returned, we see if we are done, or we set the knight back a move
            previous_move = self._check_if_finished(possible_moves)
            if type(previous_move) is str and "Finished" == previous_move:
                return self.knight.visited_positions
            move_combos = self._create_second_moves(possible_moves)    
            if move_combos == []:
                previous_move = self.knight.retrace()
            else:    
                previous_move = self._choose_best_move(move_combos)

    #untested
    def _create_second_moves(self, possible_moves):
        move_combos = [] #this will hold all 2 move combinations to be selected by the knight by weight
        for i in possible_moves:
            #print knight.get_current_position(), i
            move = (i,) #each of these will hold a 2 move combination
            trial_knight1 = Knight(i)
            trial_knight1.visited_positions = self.knight.visited_positions[:]
            k1_possible_moves = trial_knight1.get_possible_moves(self.knight.get_current_position())                
            for j in k1_possible_moves:
                #print "\t", j
                moves = move + (j,)   
            move_combos.append(moves)
        return move_combos

    #untested
    def _choose_best_move(self, move_combos):
        good_moves = self._get_weights(move_combos)
        #print good_moves
        for move in good_moves:
            print "Moving to", move
            self.knight.record_visited_position(move)
        previous_move = good_moves[0]
        if good_moves[1] in self.knight.trials.get(previous_move, set()):
            previous_move = self.knight.retrace()
        else:
            self.knight.set_position(good_moves[1])
        failed_moves = self.knight.trials.get(previous_move, set())
        failed_moves.add(good_moves[1])
        self.knight.trials[previous_move] = failed_moves
        
        return previous_move        

    def _check_if_finished(self, possible_moves):
        previous_move = None
        if len(possible_moves) == 0:
            if len(self.knight.visited_positions) < self.board.size:
                previous_move = self.knight.retrace()
                self._check_tour(previous_move)
            else:
                return "Finished"
        return previous_move

    def _check_tour(self, previous_move):
        if previous_move == self.start_position:
            print "no solution found"
            exit(2)        

    def _get_weights(self, move_combos):
        #two positions will be returned that have a weight less than or equal to other possible position combinations
        weights = {}
        for i in move_combos:
            #print "getting weights"
            #print "one move combo", i
            #print i[0], i[1]
            weight = i[0].weight + i[1].weight
            weights[weight] = i
        #print "\t", weights    
        return weights.get(min(weights),None) #maybe i want max here but I doubt it

def main(rows=6, columns=6, starting_location="2.6", verbose=False):
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
    if verbose == None:
        verbose = raw_input("would you like to display the ordered coordinates for the final tour? (y/n)\n")
        if verbose.lower() == "y" or verbose.lower() == "yes":
            verbose = True
        else:
            verbose = False
    t = Tour(rows, columns, starting_location, verbose)
    result = t.start_tour()
    
#"""
if __name__ == "__main__":
    print "Welcome to Knights Tour!\n"
    print "\tType 'e' or 'exit' to skip the prompts...\n"
    main()
#"""

def test_data(rows=6, columns=6, row=2, column=6, start="4.5"):
    tour = Tour(rows, columns, start)
    board = Board(rows, columns)
    position = Position(row, column, board)
    knight = Knight(position)
    return tour, board, position, knight

