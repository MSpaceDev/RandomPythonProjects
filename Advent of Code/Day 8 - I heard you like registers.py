from __future__ import division

regs = {}
storeRegVals = []

def addToMap(var):
    if ((var in regs) == False):
        regs.update({var : 0})

def getValues(string):
    function = string.split(" ")
    function.pop(3)
    function[5] = function[5].replace("\n", "")
    return function

def applyOperation(arg, comp, oper, var, func, amount):
    curVal = regs.get(var)
    argVal = regs.get(arg)
    if (argVal > comp and oper == ">"):
        if func == "inc":
            curVal += amount
        if func == "dec":
            curVal -= amount

    if (argVal < comp and oper == "<"):
        if func == "inc":
            curVal += amount
        if func == "dec":
            curVal -= amount

    if (argVal >= comp and oper == ">="):
        if func == "inc":
            curVal += amount
        if func == "dec":
            curVal -= amount

    if (argVal <= comp and oper == "<="):
        if func == "inc":
            curVal += amount
        if func == "dec":
            curVal -= amount

    if (argVal == comp and oper == "=="):
        if func == "inc":
            curVal += amount
        if func == "dec":
            curVal -= amount

    if (argVal != comp and oper == "!="):
        if func == "inc":
            curVal += amount
        if func == "dec":
            curVal -= amount

    regs.update({var : curVal})
    storeRegVals.append(regs.get(var))

def interperet(string):
    values = getValues(string)
    applyOperation(values[3], int(values[5]), values[4], values[0], values[1], int(values[2]))

with open("Advent of Code/Day 8 - Puzzle Input") as f:
    content = f.readlines()
    # Assign all vars to map
    for string in content:
        values = getValues(string)
        addToMap(values[0])
    # Interpret "code"
    for string in content:
        interperet(string)

    print("Max Register: ",max(regs.values())," Max Register ALLTIME: ",max(storeRegVals))