#!/usr/bin/python

start = 1
end = 0
swolves = 0
ewolves = 0
schick = 0
echick = 0

def boat(wolf, chicken):
    if wolf > 2:
        return
    elif chicken > 2:
        return
    if start == 1:
        start = 0
        end = 1
        ewolves += wolf
        echick += chicken
        swolves -= wolf
        schick -= chicken
    elif end == 1:
        start = 1
        end = 0
        swolves += wolf
        schick += chicken
        ewolves -= wolf
        echick -= chicken

def check():
    if swolves > schick:
        print("game over")
        return
    elif ewolves > echick:
        print("game over")
        return

def init():
    game = open("test.txt","r")
    gamelines = game.readlines()
    print(gamelines)
    finish = gamelines(0).split(",")
    begin = gamelines(1).split(",")
    print(begin)
    print(finish)