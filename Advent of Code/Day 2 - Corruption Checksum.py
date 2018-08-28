from __future__ import division

arrVal = []
arrSum = []
arrDiv = []

def checkDivisible(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            if(i == j):
                continue
            divVal = arr[i] / arr[j]
            if(divVal.is_integer()):
                return divVal
    return 0

with open("Advent of Code/Day 2 - Puzzle Input") as f:
    content = f.readlines()
    for s in content:
        s = s.split("\t")
        for i in range(len(s)):
            s[i] = int(s[i])
        arrVal.append(s)

    # Part 1
    for i in range(0, len(arrVal)):
        maxVal = max(arrVal[i])
        minVal = min(arrVal[i])
        diff = maxVal - minVal
        arrSum.append(diff)

    # Part 2
    for i in range(len(arrVal)):
        arrDiv.append(checkDivisible(arrVal[i]))

    print("Difference between: ", sum(arrSum))
    print("Sum of divisibles:  ", sum(arrDiv))