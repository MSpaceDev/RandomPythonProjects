from numpy import *

def main(pInput, spiralSize, puzzleActive):
    spiralCenter = int(spiralSize / 2)
    spiral = [[0] * (spiralSize + 1) for _ in range(spiralSize)]

    # 0: Right
    # 1: Up
    # 2: Left
    # 3: Down
    d = 0
    step = 1
    c = 2

    i = j = spiralCenter
    spiral[spiralCenter][spiralCenter] = 1
    for _ in range(spiralSize - 1):
        for t in range(2):
            for n in range(step):
                if d == 0:
                    j += 1
                if d == 1:
                    i -= 1
                if d == 2:
                    j -= 1
                if d == 3:
                    i += 1
                try:
                    spiral[i][j] = spiral[i + 1][j] + spiral[i - 1][j] + spiral[i][j + 1] + spiral[i][j - 1] + spiral[i + 1][j + 1] + spiral[i - 1][j - 1] + spiral[i + 1][j - 1] + spiral[i - 1][j + 1]
                    if (spiral[i][j] > pInput):
                        if(puzzleActive == True):
                            print(spiral[i][j])
                            return
                except:
                    pass
            d += 1
            d %= 4
        step += 1
    printSpiral(spiral)

def printSpiral(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

spiral = main(312051, 11, False)