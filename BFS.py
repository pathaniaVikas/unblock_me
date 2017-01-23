
#---------|---------|--|--|------#
#         |         |U |L |      |  /
#---------|---|     |N |O |      | /
#             |     |B |C |      |/  
#---------|---|     |__|K |      -----\
# PULL OUT|            |  |      -----/
#---------|    __      |__|       \
#             |M |               | \
#             |E |               |  \
#             |  |               |
#-------------|--|---------------#

# 0 for empty
# 2,2 for horizontal block of size 2
# 3,3 for horizontal block of size 3
# 4,4 for vertical block of size 2
# 6,6 for vertical block of size 3
# 5,5 for red horizontal block which we need to move out

import hashlib
row1= [3,3,3,0,0,4]
row2= [4,3,3,3,0,4]
row3= [4,0,4,5,5,4]
row4= [2,2,4,6,0,4]
row5= [0,0,0,6,2,2]
row6= [3,3,3,6,0,0]

puzzle_map_start = [row1, row2, row3, row4, row5, row6]

# Queue for breadth first search
from queue import Queue
states_queue = Queue()
visited_states_dict = {}
relation_dict = {}

def check_final_state(puzzle_map):
    if puzzle_map[2][4] == 5 and puzzle_map[2][5] == 5: 
        return True
    else:
        return False

def new_map(puzzle_map):
    n_map = []
    for row in puzzle_map:
        new_row = []
        for val in row:
            new_row.append(val)
        n_map.append(new_row)
    return n_map

def add_relation_dict(child, parent):
    '''
    This dict is used to track parent relationship info which is used in tracking path
    '''
    hs = hashlib.md5(str(child).encode())
    relation_dict[hs.hexdigest()] = parent


def add_new_state(new_state, parent_state):
    '''
    Using md5 checksum of map as key in dictionary since python does not
    entertain lists as keys in dict as lists are mutable.
    '''
    hs = hashlib.md5(str(new_state).encode())
    if visited_states_dict.get(hs.hexdigest()):
        return
    #print(new_state)
    visited_states_dict[hs.hexdigest()] = 1
    states_queue.put(new_state)
    add_relation_dict(new_state, parent_state)
    return

def check_below(puzzle_map, row, col):
    if puzzle_map[row+1][col] == 4 :
        new_state = new_map(puzzle_map)
        new_state[row][col] = 4
        new_state[row+2][col] = 0
        add_new_state(new_state, puzzle_map)
    elif puzzle_map[row + 1][col]==6:
        new_state = new_map(puzzle_map)
        new_state[row][col] = 6
        new_state[row+3][col] = 0
        add_new_state(new_state, puzzle_map)

def check_right(puzzle_map, row, col):
    if puzzle_map[row][col+1] == 2 :
        new_state = new_map(puzzle_map)
        new_state[row][col] = 2
        new_state[row][col+2] = 0
        add_new_state(new_state, puzzle_map)
    elif puzzle_map[row][col+1]==3:
        new_state = new_map(puzzle_map)
        new_state[row][col] = 3
        new_state[row][col+3] = 0
        add_new_state(new_state, puzzle_map)

    if puzzle_map[row][col+1] == 5 :
        new_state = new_map(puzzle_map)
        new_state[row][col] = 5
        new_state[row][col+2] = 0
        add_new_state(new_state, puzzle_map)

def check_left(puzzle_map, row, col):
    if puzzle_map[row][col-1] == 2 :
        new_state = new_map(puzzle_map)
        new_state[row][col] = 2
        new_state[row][col-2] = 0
        add_new_state(new_state, puzzle_map)
    elif puzzle_map[row][col-1]==3:
        new_state = new_map(puzzle_map)
        new_state[row][col] = 3
        new_state[row][col-3] = 0
        add_new_state(new_state, puzzle_map)

    if puzzle_map[row][col-1] == 5 :
        new_state = new_map(puzzle_map)
        new_state[row][col] = 5
        new_state[row][col-2] = 0
        add_new_state(new_state, puzzle_map)

def check_up(puzzle_map, row, col):
    if puzzle_map[row-1][col] == 4 :
        new_state = new_map(puzzle_map)
        new_state[row][col] = 4
        new_state[row-2][col] = 0
        add_new_state(new_state, puzzle_map)
    elif puzzle_map[row-1][col]==6:
        new_state = new_map(puzzle_map)
        new_state[row][col] = 6
        new_state[row-3][col] = 0
        add_new_state(new_state, puzzle_map)

def make_move(puzzle_map):
    #search for zeroes in puzzle map and change state
    row = 0
    while row <=5:
        col = 0
        while col <= 5:
            if puzzle_map[row][col] == 0:
                # implement move logic here
                if row==0:
                    if col == 0:
                        # check for right and below only
                        check_right(puzzle_map, row, col)
                        check_below(puzzle_map, row, col)
                    elif col == 5:
                        # check for left and below only
                        check_left(puzzle_map, row, col)
                        check_below(puzzle_map, row, col)
                    else:
                        # check for left, right and below only
                        check_left(puzzle_map, row, col)
                        check_right(puzzle_map, row, col)
                        check_below(puzzle_map, row, col)
                elif row==5:
                    if col == 0:
                        # check for right and up only
                        check_right(puzzle_map, row, col)
                        check_up(puzzle_map, row, col)
                    elif col == 5:
                        # check for left and up only
                        check_left(puzzle_map, row, col)
                        check_up(puzzle_map, row, col)
                    else:
                        # check for left, right and up only
                        check_left(puzzle_map, row, col)
                        check_right(puzzle_map, row, col)
                        check_up(puzzle_map, row, col)
                else:
                    if col == 0:
                        # check for right, up and down only
                        check_right(puzzle_map, row, col)
                        check_up(puzzle_map, row, col)
                        check_below(puzzle_map, row, col)
                    elif col == 5:
                        # check for left, up and down only
                        check_left(puzzle_map, row, col)
                        check_up(puzzle_map, row, col)
                        check_below(puzzle_map, row, col)
                    else:
                        # check for left, right, up and down all
                        check_left(puzzle_map, row, col)
                        check_right(puzzle_map, row, col)
                        check_up(puzzle_map, row, col)
                        check_below(puzzle_map, row, col)
            col += 1
        row += 1

from queue import LifoQueue
def get_path(final_state):
    final_path = LifoQueue()
    final_path.put(final_state)

    hs = hashlib.md5(str(final_state).encode())

    while relation_dict[hs.hexdigest()]:
        hs = hashlib.md5(str(final_state).encode())
        parent = relation_dict[hs.hexdigest()]
        final_state = parent
        if parent:
            final_path.put(parent)

    return final_path

def print_path(final_path):
    while not final_path.empty():
        state = final_path.get()
        for row in state:
            print(row)
        print()

def start():
    add_new_state(puzzle_map_start, None)
    while not states_queue.empty():
        search_state = states_queue.get()
        if check_final_state(search_state):
            print("found answer")
            fp = get_path(search_state)
            print_path(fp)
            return
        else:
            make_move(search_state)
            
    print("No answer found ")


if __name__ == '__main__':
    start()
