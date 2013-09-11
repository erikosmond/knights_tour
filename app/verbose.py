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
        return #remove this, but change the switch 
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
            pass
            #self.final_positions(chess_piece)

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
            print "\n\n"
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
            print "\n\n"    
            #raw_input("press any key to continue")

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