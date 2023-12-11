def parse(stream):
    sequences = []
    for rawline in stream:
        line = rawline.strip()
        seq = [int(s) for s in line.split()]
        sequences.append(seq)
    return sequences