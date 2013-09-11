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

def main(rows=8, columns=8, starting_location="2.3", verbosity=73): #was 907 then 1023 then 393 then 193 then 201
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

