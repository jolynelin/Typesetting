#!/usr/bin/env python3

# Name: Jolyne Lin
# Date: Feb 21, 2023

import argparse

def format(filename, columns, k):
    """ Input:  Takes a filename, a number of columns, penalty exponent k
        Output: Prints a line with columns dots (to show permitted width)
                Prints the optimally-formatted words.
                Returns a single number, which is the optimal penalty
    """

    with open(filename, "r") as f:   # Opens the file to be read and
                                     # automatically closes it when the block ends
        # f.read() returns the file contents as one string (including newlines)
        # Then .split() splits that string into a list of words by whitespace
        listOfWords = f.read().split()

    # Now listOfWords is the list of strings (one per word)
    # to be formatted.

    # Call DP function
    n = len(listOfWords)
    dp_table = ['empty'] * n
    print_clue = ['empty'] * (n-1)
    print_stuff = []

    if listOfWords == []:
        return 0
    for i in reversed(range(n)):
        current_list = listOfWords[i:n]
        first_line = one_line(current_list, columns)
        options = ['empty'] * len(first_line)
        if columns > len(first_line[0]):
            line_use = len(first_line[0])
            option = (columns-line_use)**k
            if i+1 < n:
                option += dp_table[i+1]
            best_option = option
        for j in range(len(first_line)-1):
            line_use += len(first_line[j+1]) + 1
            option = (columns-line_use)**k
            if i+j+2 < n:
                option += dp_table[i+j+2]
            if option <= best_option:
                best_option = option
                print_clue[i] = i+j+1
        dp_table[i] = best_option
    
    print_start = 0
    print_end = print_clue[print_start] + 1
    while print_end < n:
        new_stuff = listOfWords[print_start: print_end]
        print_stuff.extend([new_stuff])
        print_start = print_end
        print_end = print_clue[print_start]+1
    new_stuff = listOfWords[print_start: print_end]
    print_stuff.extend([new_stuff])
    printDots(columns)
    output = [' '.join(i) for i in print_stuff]
    for i in range(len(output)):
        print(output[i])
    # Print the line of dots and the formatted output
    # without extra blank lines

    # Return the optimal penalty score.
    return dp_table[0]


def printDots(columns: int):
    """ Prints a sequence of dots to indicate number of columns. """
    print("." * columns)

#
# Helper Functions
#
def one_line(listOfWords, columns):
    """ Input:  Takes a list of words and a number of columns
        Output: Returns listOfWords[0:j], where j takes the largest possible value
                from 0 to len(listOfWords) such that listOfWords[0:j] fit on one line
    """
    line = []
    if columns > len(listOfWords[0]):
        line.extend([listOfWords[0]])
        columns = columns - len(listOfWords[0])
    i = 1
    while columns > 0 and i < len(listOfWords):
        columns = columns - len(listOfWords[i]) - 1
        if columns > 0:
            line.extend([listOfWords[i]])
            i += 1
    return line


if __name__ == "__main__":
    # If we ran this file directly (rather than importing it), then
    # use command-line arguments to call format, e.g.,
    #   python3 format.py huckleberry.txt 50 2

    # Command-line parsing
    #   Require user to specify filename, columns, and k on the command-line.
    parser = argparse.ArgumentParser()
    # The first command-line argument will be called "file".
    # It's a string.
    parser.add_argument("file", type=str)
    # The second command-line argument will be called "cols"
    # It's an integer.
    parser.add_argument("cols", type=int)
    # The third command-line argument will be called "power"
    # It's an integer.
    parser.add_argument("power", type=int)
    args = parser.parse_args()

    # Run the formatting code
    print(format(args.file, args.cols, args.power))
