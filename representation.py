
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
row1= [3,3,3,0,0,0]
row2= [0,0,0,0,0,4]
row3= [5,5,0,4,0,4]
row4= [0,0,0,4,0,0]
row5= [2,2,0,0,0,0]
row6= [0,0,0,0,0,0]

puzzle_map_start = [row1, row2, row3, row4, row5, row6]

# Queue for breadth first search
from queue import LifoQueue
states_queue = LifoQueue()
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
    hp = None
    # this condition is only for testing root node
    if parent:
        hp = hashlib.md5(str(parent).encode())
        hp = hp.hexdigest()
    relation_dict[hs.hexdigest()] = hp

def update_parent_dict(parent, added):
    '''
    update parent dict to reflect its total childs 
    '''
    hs = hashlib.md5(str(parent).encode())
    visited_states_dict[hs.hexdigest()] = added

def reduce_child_count(child, iteration = 0):
    '''
    update parent dict to reflect total childs remaining for processing 
    '''
    if not iteration:
        child = hashlib.md5(str(child).encode())
        child = child.hexdigest()
    parent = relation_dict[child]
    c = visited_states_dict.get(parent)
    visited_states_dict[parent] = c - 1
    if c-1 == 0:
        reduce_child_count(parent, 1)

def add_new_state(new_state, parent_state):
    '''
    Using md5 checksum of map as key in dictionary as python does not
    entertain lists as keys in dict as they are mutable.
    returns 0 if no child added or 1 otherwise
    used to track total no of child for current parent
    '''
    hs = hashlib.md5(str(new_state).encode())
    if visited_states_dict.get(hs.hexdigest()):
        return 0
    #print(new_state)
    visited_states_dict[hs.hexdigest()] = 0
    states_queue.put(new_state)
    add_relation_dict(new_state, parent_state)
    return 1

def check_right(puzzle_map, row, col, added):
    if puzzle_map[row+1][col] == 4 :
        new_state = new_map(puzzle_map)
        new_state[row][col] = 4
        new_state[row+2][col] = 0
        added += add_new_state(new_state, puzzle_map)
    elif puzzle_map[row + 1][col]==6:
        new_state = new_map(puzzle_map)
        new_state[row][col] = 6
        new_state[row+3][col] = 0
        added += add_new_state(new_state, puzzle_map)
    return added

def make_move(puzzle_map):
    #search for zeroes in puzzle map and change state
    row = 0
    # added used to count total childs added
    added = 0
    while row <=5:
        col = 0
        while col <= 5:
            if puzzle_map[row][col] == 0:
                # implement move logic here
                if row==0:
                    if col == 0:
                        # check for right and below only
                        if puzzle_map[row+1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row+2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row + 1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row+3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col+1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col+3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)

                    elif col == 5:
                        # check for left and below only
                        if puzzle_map[row+1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row+2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row + 1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row+3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col-1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col-3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                    else:
                        # check for left, right and below only
                        if puzzle_map[row+1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row+2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row + 1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row+3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col+1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col+3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col-1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col-3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                elif row==5:
                    if col == 0:
                        # check for right and up only
                        if puzzle_map[row][col+1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col+1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col+3] = 0
                            added += add_new_state(new_state, puzzle_map)
                        if puzzle_map[row-1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row-2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row-1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row-3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)

                    elif col == 5:
                        # check for left and up only
                        if puzzle_map[row-1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row-2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row-1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row-3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col-1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col-3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                    else:
                        # check for left, right and up only
                        if puzzle_map[row-1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row-2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row-1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row-3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col-1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col-3] = 0
                            added += add_new_state(new_state, puzzle_map)
                        if puzzle_map[row][col+1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col+1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col+3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                else:
                    if col == 0:
                        # check for right, up and down only
                        if puzzle_map[row][col+1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col+1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col+3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row-1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row-2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row-1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row-3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row+1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row+2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row + 1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row+3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)
                    elif col == 5:
                        # check for left, up and down only
                        if puzzle_map[row][col-1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col-1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col-3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row-1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row-2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row-1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row-3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row+1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row+2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row + 1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row+3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                    else:
                        # check for left, right, up and down all
                        if puzzle_map[row][col-1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col-1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col-3] = 0
                            added += add_new_state(new_state, puzzle_map)
                            
                        if puzzle_map[row-1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row-2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row-1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row-3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row+1][col] == 4 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 4
                            new_state[row+2][col] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row + 1][col]==6:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 6
                            new_state[row+3][col] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 2 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 2
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)
                        elif puzzle_map[row][col+1]==3:
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 3
                            new_state[row][col+3] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col+1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col+2] = 0
                            added += add_new_state(new_state, puzzle_map)

                        if puzzle_map[row][col-1] == 5 :
                            new_state = new_map(puzzle_map)
                            new_state[row][col] = 5
                            new_state[row][col-2] = 0
                            added += add_new_state(new_state, puzzle_map)
            col += 1
        row += 1
    return added

path_list = []

def print_path():
    for st in path_list:
        hs = hashlib.md5(str(st).encode())
        if visited_states_dict[hs.hexdigest()] > 0:
            for s in st:
                print(s)
            print()

def start():
    add_new_state(puzzle_map_start, None)
    while not states_queue.empty():
        search_state = states_queue.get()
        path_list.append(search_state)
        if check_final_state(search_state):
            print("found answer")
            print_path()
            return
        else:
            added = make_move(search_state)
            if not added:
                # if no child added then its the terminating node just pop this entry from list 
                # and reduce "in processing child count" of parent
                path_list.pop()
                reduce_child_count(search_state)
            else:
                # else update parents dict to reflect newly added child count
                update_parent_dict(search_state, added)

    print("No answer found ")


if __name__ == '__main__':
    start()
