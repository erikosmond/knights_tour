from app.board import Board, Position
from app.pieces import Knight
from app.verbose import Verbose
from app.move import Move

class MoveError(Exception):
    
    def __init__(self, position):
        print "Knight can not move to", position, " as it has already been visited."
    


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
            #garner stats
            largest_tour = self.verbosity.min_max(self, largest_tour)
            self.verbosity.potential_OBOB(self)
            self.verbosity.progress(count)
            if len(self.knight.visited_positions) < 4:
                largest_tour = len(self.knight.visited_positions)
            
            #find the next move
            ##REMOVE - i should be able to get rid of all this previous move business as all the checking happens elsewhere - I still need to call some form of this method though
            possible_positions = self.knight.get_possible_moves()
            self.verbosity.possible_moves(self.knight.get_current_position(), possible_positions)
            if len(possible_positions) == 0:
                    count += 1
                    self.knight.retrace()
                    continue
                
            initial_moves = []
            for position in possible_positions: #the position already has a weight when it's created
                move = Move(position, self.knight.get_visited_positions()[:])
                initial_moves.append(move)
            best_move = Move.choose_best_move(initial_moves)
            if not self.knight.set_position(best_move.get_position()):
                raise MoveError(best_move.get_position())
            
            """    
            else:
                move_options = {}
                for i in possible_moves:
                    num_moves = len(self._create_second_moves(i))
                    #if num_moves == 0: #maybe remove this, but it should be a minor optimization
                        #continue
                    move_options[num_moves] = i
                best_position = min(move_options)
                self.knight.set_position(move_options[best_position])
                
                move_combos = self._create_second_moves(i)
                if len(move_combos) == 0:
                    print "move combos len is 0"
                    if self.knight.set_position(self.knight.get_current_position()) == True: #this can't be right
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
            #"""
            #previous_move = self._choose_best_move(move_combos)
            count += 1
        return self.knight
        #return self.knight.get_visited_positions()

    def _end_of_game(self, possible_moves):
        if len(possible_moves) == 0 and len(self.knight.visited_positions) == self.board.size:
            return "Finished" 
        else:
            return self.knight.retrace()
        

    #untested
    def _create_second_moves(self, i):
        move_combos = [] #this will hold all 2 move combinations to be selected by the knight by weight
        move = (i,) #each of these will hold a 2 move combination
        trial_knight1 = Knight(i, self.verbosity.verbose_int)
        trial_knight1.visited_positions = self.knight.visited_positions[:]
        k1_possible_moves = trial_knight1.get_possible_moves(self.knight.get_current_position())
        """
        if len(k1_possible_moves) == 0:
            previous_move = self._end_of_game(possible_moves)
            if type(previous_move) == type(self.knight.current_position):
                return move_combos
            elif self._end_of_game(possible_moves) == "Finished":
                return self.knight.visited_positions
        #"""
        self.verbosity.possible_moves(i, k1_possible_moves)    
        for j in k1_possible_moves:
            moves = move + (j,)   
            move_combos.append(moves) # I just indented this on 9-10-13 7:20pm
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