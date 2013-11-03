from board import Position
from pieces import Knight

class Move(object):
    
    @classmethod
    def choose_best_move(self, moves, end_positions):
        possibilities = {}
        for move in moves:
            moves_by_num = possibilities.get(move.get_num_possible_moves(), tuple())
            moves_by_num = moves_by_num + (move,)
            possibilities[move.get_num_possible_moves()] = moves_by_num
            #get the move with the least possible position, if there's more than one, go by weight
        fewest_moves = min(possibilities)
        lowest_weight = 20
        best_move = None
        for move in possibilities[fewest_moves]:
            move_weight = move.get_position().get_weight()
            if end_positions != None:
                move_weight = move._check_closed_tour(move_weight, end_positions)
            if move_weight != None and move_weight < lowest_weight:
                lowest_weight = move_weight
                best_move = move
        return best_move
    
    def __init__(self, position, visited_positions):
        self.knight = Knight(position)
        self.knight.visited_positions = visited_positions
        self.position = position
        ###is this the source of the bug somehow?
        self.possible_moves = self.knight.get_possible_moves() #should be able to remove previous position/ None

    def _check_closed_tour(self, move_weight, end_positions):
        if self.get_position() in end_positions:
            move_weight += 10
        return move_weight

    def get_position(self):
        return self.position
    
    def get_num_possible_moves(self):
        return len(self.possible_moves)
    
    def print_possible_moves(self):
        for i in self.get_possible_moves():
            print "\t", i
        return "end of possible moves"
        
    def get_possible_moves(self):
        return self.possible_moves
    
    
    def __str__(self):
        return self.position.__str__()
    
    