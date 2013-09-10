from app.board import Board, Position
from app.pieces import Knight
from app.verbose import Verbose

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