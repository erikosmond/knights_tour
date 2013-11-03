from app.board import Board, Position
from app.pieces import ChessPiece, Knight, GameError
from app.verbose import Verbose
from app.tour import Tour

import time
import json
import logging
import multiprocessing
        
#I should consider logging so I can view STDOUT and have it write to disk 

def main(rows=12, columns=12, starting_location="8.8", save=False, verbosity=512, closed=True): #512 is just completed tour, 64 is what i want for testing, 577 is good, was 907 then 1023 then 393 then 193(good for full test) then 201 then 73
#def main(rows=None, columns=None, starting_location=None, save=None, closed=None, verbosity=None):
    if None in [rows, columns, starting_location, verbosity]:
        print "\tEnter 'e' or 'exit' to skip the prompts and exit the program...\n"
    if rows == None:
        rows = raw_input("How many rows would you like on the chess board?\n")
        if rows.lower() == "e" or rows.lower() == "exit":
            return
    if columns == None:
        columns = raw_input("How many columns would you like on the chess board?\n")
        if columns.lower() == "e" or columns.lower() == "exit":
            return
    if starting_location == None:
        starting_location = raw_input("Which coordinate which you like to be the starting location?  (please enter in the format of row.column, eg. 4.5)\n")
        if starting_location.lower() == "e" or starting_location.lower() == "exit":
            return
    if save == None:
        save_input = raw_input("Would you like to save your tour to a file? (y/n)\n")
        if save_input.lower() == "y" or save_input.lower() == "yes":
            save = True
        elif save_input.lower() == "e" or save_input.lower() == "exit":
            return
    if closed == None:
        closed_input = raw_input("Would you like the tour to form a loop from start to end (a closed tour)? (y/n)\n")
        if closed_input.lower() == "y" or closed_input.lower() == "yes":
            save = True
        elif closed_input.lower() == "e" or closed_input.lower() == "exit":
            return
    if verbosity == None:
        verbosity = raw_input("would you like to display the ordered coordinates for the final tour? (y/n)\n")
        try:
            verbosity = int(verbosity)
        except Exception:
            pass
        if verbosity.lower() == "y" or verbosity.lower() == "yes":
            verbosity = 512
        elif type(verbosity) is int:
            verbosity = verbosity
        else:
            verbosity = 0
    print "\tSearching for solutions...\n"
    start_time = time.time()
    
    t = Tour(rows, columns, starting_location, verbosity, closed)
    #try:
        #results = t.run
    knight, count, board, end_time = t.run()
        #run multiple instances of the tour, and the one with the smallest difference between
        #their biggest tour and rebound down to smallest  visited positions.
        #big rebounds means a lot of possiblilities were ruled out
    print "\tFound result!"
    table = board.html_board()
     
    v = Verbose(verbosity)
    if verbosity >= 512:
        print "\tThe simulation lasted", str(count), "moves and took", str(round(end_time, 3)), "seconds"
        v.board(knight, final=True)
    v.progress(count, knight)
    
    if save == True:
        final_tour = knight.get_tour()
        json_tour = json.dumps(final_tour)
        timestamp = str(int(time.time()))
        fp = open("./tour-" + timestamp + ".json", "w+")
        json.dump(json_tour, fp)
        fp.close()
    
    
#"""
if __name__ == "__main__":
    print "Welcome to Knights Tour!\n"
    try:
        main()
    except GameError:
        pass
#"""

def test_data(rows=3, columns=3, row=2, column=6, start="4.5"):
    tour = Tour(rows, columns, start, verbosity=0)
    board = Board(rows, columns, tour.verbosity.verbose_int)
    position = Position(row, column, board, tour.verbosity.verbose_int)
    knight = Knight(position, tour.verbosity.verbose_int)
    return tour, board, position, knight

