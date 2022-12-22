def delta(seq):
    for this, next in zip(seq, seq[1:]):
        yield next - this


def main():
    seq = [1,3,5,5,9]
    deltas = list(delta(seq))
    print(seq, deltas)

if __name__ == '__main__':
    main()