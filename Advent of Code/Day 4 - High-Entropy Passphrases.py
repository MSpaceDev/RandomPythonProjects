def isAnagram(i, j):
    i = sorted(i)
    j = sorted(j)
    if i==j:
        return True
    return False

def isDupe(arr):
    for j in range(len(arr)):
        for k in range(len(arr)):
            if j==k:
                continue
            if(isAnagram(arr[j], arr[k])):
                return False
    return True

with open("Advent of Code/Day 4 - Puzzle Input") as f:
    content = f.readlines()
    allWords = []

    for s in content:
        s = s.split(" ")
        s[len(s) - 1] = s[len(s) - 1].replace("\n", "")
        allWords.append(s)

    c = 0
    for i in range(len(allWords)):
        if(isDupe(allWords[i])):
            c += 1

    print(c)