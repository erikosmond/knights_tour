from app.board import Board, Position
from app.pieces import ChessPiece, Knight
from app.verbose import Verbose
from app.tour import Tour

import time
import logging
import multiprocessing

class GameError(Exception):
    def __init__(self):
        print "tour didn't work"
        
#I should consider logging so I can view STDOUT and have it write to disk 

def main(rows=8, columns=8, starting_location="1.1", verbosity=512): #was 907 then 1023 then 393 then 193(good for full test) then 201 then 73
#def main(rows=None, columns=None, starting_location=None, verbosity=None):
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
    print "\tCurrently searching for solutions...\n"
    start_time = time.time()
    t = Tour(rows, columns, starting_location, verbosity)
    try:
        #results = t.run
        knight, count = t.run()
        #run multiple instances of the tour, and the one with the smallest difference between
        #their biggest tour and rebound down to smallest  visited positions.
        #big rebounds means a lot of possiblilities were ruled out
    except GameError:
        print "took", time.time() - start_time
        return
    print "\tFound result!"
    print "\tThe simulation lasted", str(count), "moves."
    if verbosity == 512:
        v = Verbose(verbosity)
        v.final_positions(knight)
    #for i in knight.get_visited_positions():
        #print i
    print "took", time.time() - start_time
    return knight.get_visited_positions()
    
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

