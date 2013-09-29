from verbose import Verbose
import time

class Board(object):

    def __init__(self, rows, columns, verbosity=0):
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = self.rows * self.columns
        #for both row and column, calculate how many moves a position is away from the edge of the board then add 1 
        self.moves = {2:2, 3:3, 4:4, 5:6, 6:8} #shows how many moves are possible given how close the position is to the edge of the board
        self.verbosity = Verbose(verbosity)

    def get_weight(self, row, column):
        #for now, if a chess piece is 3 deep, it's weighted the same as all other inner pieces, hence limiting the depth to a max of 3
        row_depth = min(row, self.rows-row+1, 3)
        column_depth = min(column, self.columns-column+1, 3)
        return self.moves.get(column_depth + row_depth, None)
    
    def html_board(self):
        coordinates = []
        for row in range(1, self.rows+1):
            for column in range(1, self.columns+1):
                p = Position(row, column, self)
                coordinates.append(p)
	css = self.get_css()
        table = [r'<table border=1 width="400" height="400" table-layout="fixed">']
        row = 0
        for p in coordinates:
            square = r'OddSquare'
            if p.row > row:
                if row != 0:
                    table.append(r'</tr>')
                row = p.row
                table.append(r'<tr>')    
            if (p.row + p.column) % 2 == 0:
                square = r'EvenSquare'
            table.append(r'<td class="'+ square + r'" id="'+p.str_coordinate + r'"</td>')
        table.extend([r'</tr>', r'</table>'])
	css.extend(table)
	html_table = ''.join(css)
        timestamp = str(int(time.time()))
	#fp = open("./ChessBoard-" + timestamp + ".html", "w+")
        #fp.write(html_table)
        #fp.close()
	return html_table
		
    def get_css(self):
	css = [
	    r'<style>',
	    r'.EvenSquare {',
	    r'padding: 0;',
	    r'background: #55c1eb;',
	    r'color: #55c1eb;',
	    r'padding-bottom: 0px;',
	    r'table-layout:fixed;',
	    r'width:100px;',
	    r'overflow:hidden;',
	    r'font-size: large;',
	    r'text-align: center;',
	    r'word-wrap: break-word;',
	    r'}',
	    r'.OddSquare {',
	    r'padding: 0;',
	    r'background: #d10606;',
	    r'color: #d10606;',
	    r'padding-bottom: 0px;',
	    r'table-layout:fixed;',
	    r'width:100px;',
	    r'overflow:hidden;',
	    r'font-size: large;',
	    r'text-align: center;',
	    r'word-wrap: break-word;',
	    r'</style>',
	]
	return css
	

class Position(object):

    def __init__(self, row, column, board, verbosity=0):
        self.row = row
        self.column = column
        self.coordinate = (row, column)
        self.str_coordinate = str(row)+'.'+str(column)
        self.board = board
        self.verbosity = Verbose(verbosity)
        self.fits_on_board = self._check_board()
        self.failures = []
        self.retrace = False
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
    
    def _check_board(self):
        if not 0 < self.row <= self.board.rows:
                return False
        if not 0 < self.column <= self.board.columns:
                return False
        return True

    def record_failed_position(self, position):
        self.failures.append(position)
        
    def get_weight(self):
        return self.weight
    
    def set_retrace(self):
        self.retrace = True
    
    def check_failed_position(self, position):
        if position in self.failures:
            return True
        return False