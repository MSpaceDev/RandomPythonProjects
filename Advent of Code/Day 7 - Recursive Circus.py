def removeSingles(arr):
    noSingles = []
    for s in arr:
        s = s.replace("\n", "")
        if (s.find("->") != -1):
            noSingles.append(s)
    noSingles = getParentAndChildren(noSingles)
    return noSingles

def getParentAndChildren(arr):
    branch = []
    for s in arr:
        a = s[s.find(">") + 2:]
        child = a.split(", ")
        parent = s[:s.find(" ")]
        child.insert(0, parent)
        branch.append(child)
    return branch

def getParentsAsChildren(arr):
    parentsAsChildren = []
    for i in range(len(arr)):
        for j in range(1, len(arr)):
            for k in range(len(arr[j])):
                if (i == j):
                    continue
                if(arr[i][0] == arr[j][k]):
                    parentsAsChildren.append(arr[i][0])
    return parentsAsChildren

def getAllParents(arr):
    parents = []
    for i in range(len(arr)):
        parents.append(arr[i][0])
    return parents

def findBase(arr1, arr2):
    for s in arr1:
        arr2.remove(s)
    return arr2[0]

with open("Advent of Code/Day 7 - Puzzle Input", "r") as f:
    content = f.readlines()

    branch = removeSingles(content)
    print(findBase(getParentsAsChildren(branch), getAllParents(branch)))