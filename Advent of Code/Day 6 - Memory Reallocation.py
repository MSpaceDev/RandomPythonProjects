from __future__ import division

def toString(a):
    string = ""
    for i in a:
        string += str(i)
        string += " "
    return string

var = []
memory = []
for line in open("Advent of Code/Day 6 - Puzzle Input"):
    var.append(line.split("\t"))
for i in var[0]:
    memory.append(int(i))

memory.clear()
memory = [3, 0, 0, 0]
memoryConfigs = []

memoryConfigs.append(toString(memory))
steps = 0
isRunning = True

while (isRunning == True):
    maxMem = max(memory)
    allocAmount = int(maxMem / (len(memory) - 1))
    removeAmount = int(allocAmount * (len(memory) - 1))
    indexOfMax = memory.index(maxMem)

    string = ""
    for i in range(len(memory)):
        if (i==indexOfMax):
            memory[i] -= removeAmount
            continue
        memory[i] += allocAmount

    memoryConfigs.append(toString(memory))
    steps += 1

    print (memoryConfigs)

    for i in range(len(memoryConfigs)):
        for j in range(len(memoryConfigs)):
            if (i==j):
                continue
            if (memoryConfigs[i] == memoryConfigs[j]):
                print(steps)
                isRunning = False
                break