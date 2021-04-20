#!/usr/bin/python

import sys

startfile = sys.argv[1]
endfile = sys.argv[2]
mode = sys.argv[3]
output = sys.argv[4]
actions = [[1,0],[2,0],[0,1],[1,1],[0,2]]

class bank:
    boat = 0
    w = 0
    c = 0
    parent = None
    a = None
    def p(self):
        print("boat ", self.boat)
        print("wolves ", self.w)
        print("chickens", self.c)
        print("action", self.a)

    def copy(self, newbank):
        newbank.c = self.c
        newbank.w = self.w
        newbank.boat = self.boat

    def check(self, goal):
        if self.boat == goal.boat and self.w == goal.w and self.c == goal.c:
            return 1
        else:
            return 0

    def write(self, file):
        file.write("Action: ")
        file.write(str(self.a))
        file.write("\nBoat: ")
        file.write(str(self.boat))
        file.write("    Chickens: ")
        file.write(str(self.c))
        file.write("    Wolves: ")
        file.write(str(self.w))
        file.write("\n")  

def act(state, action):
    #print(type(state[0]))
    new_left = bank()
    new_right = bank()
    new_left.c = state[0].c
    new_left.w = state[0].w
    new_left.boat = state[0].boat
    new_right.c = state[1].c
    new_right.w = state[1].w
    new_right.boat = state[1].boat
    new_left.parent = state[0]
    new_right.parent = state[1]
    new_left.a = action

    if new_left.boat == 1:
        if new_left.c - action[0] < 0:
            return 0
        elif new_left.w - action[1] < 0:
            return 0
        new_left.c -= action[0]
        new_left.w -= action[1]
        new_left.boat = 0
        new_right.c += action[0]
        new_right.w += action[1]
        new_right.boat = 1
    elif new_right.boat == 1:
        if new_right.c - action[0] < 0:
            return 0
        elif new_right.w - action[1] < 0:
            return 0
        new_left.c += action[0]
        new_left.w += action[1]
        new_left.boat = 1
        new_right.c -= action[0]
        new_right.w -= action[1]
        new_right.boat = 0
    newstate = [new_left, new_right]
    if(check(newstate, action)):
        #print("eaten")
        #new_left.p()
        #new_right.p()
        return 0
    return newstate

def check(newstate,action):
    if newstate[0].c < newstate[0].w and newstate[0].c > 0:
        return 1
    elif newstate[1].c < newstate[1].w and newstate[1].c > 0:
        return 1
    else:
        return 0

def init(left, right, goal):
    game = open(startfile,"r")
    gamelines = game.readlines()
    finish = gamelines[0].split(",")
    begin = gamelines[1].split(",")
    finish[2] = finish[2].strip("\n")
    right.c = int(begin[0])
    right.w = int(begin[1])
    right.boat = int(begin[2])
    left.c = int(finish[0])
    left.w = int(finish[1])
    left.boat = int(finish[2])
    game.close()
    goals = open(endfile, "r")
    goaline = goals.readlines()
    end = goaline[0].split(",")
    end[2] = end[2].strip("\n")
    goal.c = int(end[0])
    goal.w = int(end[1])
    goal.boat = int(end[1])
    goals.close()

def search(state, goal):
    been = []
    size = 0
    depth = 1
    frontier = []
    left = bank()
    right = bank()
    state[0].copy(left)
    state[1].copy(right)
    current = [left, right]
    frontier = front(current)
    index = 0
    while 1:
        if frontier == []:
            print("All nodes expanded")
            sys.exit()
        s = frontier[0]
        #print("left")
        #s[0].p()
        #print("right")
        #s[1].p()
        if s[0].c == goal.c and s[0].w == goal.w:
            solution = []
            while s[0].parent:
                solution.append(s[0])
                s[0] = s[0].parent
                depth += 1
            print("solution found at depth ", depth, "Nodes explored:", size)
            show(solution, depth, size)
            sys.exit()
        else:
            if mode == "bfs":
                temp = []
                size += 1 
                temp = front(s)
                #trying to check if I've visited a node takes longer to check than it does to just look through them all (at least in smaller cases)
                #for i in t:
                #    if i in been:
                #        print("copy")
                #    else:
                #        temp.append(i)   
                #if temp != []:
                frontier.extend(temp)
                been.append(frontier.pop(0))

            elif mode == "dfs":
                size += 1
                temp = front(s)
                print(s[0].a)
                if temp != []:
                    been.append(frontier.pop(0))
                    j = 0
                    for i in temp:
                        #print(type(i[0]))
                        if i[0].c == s[0].c and i[0].w == s[0].w and i[1].c == s[1].c and i[1].w == s[1].w:
                            temp.pop(j)
                            j += 1
                            continue
                        else:
                            if(size < 500):
                                frontier = temp + frontier

            elif mode == "iddfs":
                size += 1
                temp = front(s)
                if temp != []:
                    frontier.extend(temp)
                been.append(frontier.pop(0))

            elif mode == "a*":
                print("hi")
            
    
def front(state):
    front = []
    for a in actions:
        test = act(state, a)
        if test != 0:
            front.append(test)
    return front

def show(solution, depth, size):
    res = open(output,"w")
    solution.reverse()
    res.write("--Method ")
    res.write(mode)
    res.write("\n")
    res.write("   Nodes explored: ")
    res.write(str(size))
    res.write("Nodes in path: ")
    res.write(str(depth))
    res.write("\n")
    for sol in solution:
        sol.write(res)
        sol.p()
    res.close()

def main():
    print "---starting---"
    left = bank()
    right = bank()
    goal = bank()
    init(left, right, goal)
    state = [left,right]
    solution = search(state,goal)


main()
