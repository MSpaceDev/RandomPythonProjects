import math

puzzleInput = 347991

seqArr = []

def getSequenceValue(puzzleInput):
    cornerValue = 0
    i = 1
    while(puzzleInput >= cornerValue):
        cornerValue = math.pow(i, 2) + 1
        i += 2

    return i-2

def getCornerValue(puzzleInput):
    cornerValue = 0
    i = 1
    while (puzzleInput >= cornerValue):
        cornerValue = math.pow(i, 2) + 1
        i += 2

    return math.pow(i - 4, 2) + 1

def getSequenceFromValue(cornerValue):
    seqOrigin = int(cornerValue / 2)
    seqMax = seqOrigin * 2
    seqArr.clear()
    addSeq = False

    for i in range(seqMax + 1):
        if(addSeq == False):
            seqVal = seqMax - i
            if seqVal == seqOrigin:
                addSeq = True
        else:
            seqVal = i
        seqArr.append(seqVal)
    seqArr.pop(0)
    return seqArr

def getStepsFromSequence(sequence, cornerValue, puzzleInput):
    while(True):
        for d in sequence:
            if cornerValue == puzzleInput:
                return d
            cornerValue += 1

sequence = getSequenceFromValue(getSequenceValue(puzzleInput))
print(getStepsFromSequence(sequence, getCornerValue(puzzleInput), puzzleInput))