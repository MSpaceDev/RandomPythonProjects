import math

oldPos = 0
arrNum = []
with open("Advent of Code/Day 5 - Puzzle Input") as f:
    content = f.readlines()
    for s in content:
        s = s.replace("\n", "")
        arrNum.append(int(s))

    i = 0
    steps = 0
    while(True):
        try:
            oldPos = i
            i += arrNum[i] # jump
            if(arrNum[oldPos] >= 3):
                arrNum[oldPos] -= 1  # decrement value
            else:
                arrNum[oldPos] += 1 # increment value
            steps += 1
        except IndexError:
            print(steps)
            break