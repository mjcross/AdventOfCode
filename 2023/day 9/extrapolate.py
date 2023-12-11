def seqAllZero(seq):
    for item in seq:
        if item != 0:
            return False
    else:
        return True


def makeDiffs(seq):
    diff = [seq]
    while not seqAllZero(diff[-1]):
        diff.append([diff[-1][i] - diff[-1][i-1] for i in range(1, len(diff[-1]))])
    return diff


def extrapolate(seq):
    diffs = makeDiffs(seq)
    for i in reversed(range(len(diffs)-1)):
        # forward
        diffs[i].append(diffs[i][-1] + diffs[i+1][-1])
        # reverse
        diffs[i].insert(0, diffs[i][0] - diffs[i+1][0])
    return diffs[0][-1], diffs[0][0]
