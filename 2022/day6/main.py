from collections import deque

tests = [
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', (7, 19)),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', (5, 23)),
    ('nppdvjthqldpwncqszvftbrmjlhg', (6, 23)),
    ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', (10, 29)),
    ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', (11, 26))]


def detectheader(symbols, packetlen):
    dq = deque(maxlen=packetlen)
    for count, symbol in enumerate(symbols):
        dq.append(symbol)
        if len(set(dq)) == packetlen:
            return(count + 1)


def main():
    for input, results in tests:
            assert detectheader(input, packetlen=4) == results[0]
            assert detectheader(input, packetlen=14) == results[1]

    with open('input.txt') as inFile:
        symbols = inFile.readline()
        print('part1', detectheader(symbols, packetlen=4))
        print('part2', detectheader(symbols, packetlen=14))

if __name__ == '__main__':
    main()