digit_value = {
    f'{i}': i for i in range(10)
}

digit_words = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine']
word_value = {
    word: index for index, word in enumerate(digit_words) 
}

digit_or_word_value = digit_value | word_value

def part1(stream):
    sum = 0
    for line in stream:
        first = last = None
        for char in line:
            if char in digit_value:
                n = digit_value[char]
                if not first:
                    first = n
                last = n
        sum += first * 10 + last
    return sum

def part2(stream):
    sum = 0
    for rawLine in stream:
        line = rawLine.strip().lower()
        firstPos = lastPos = None
        for symbol in digit_or_word_value.keys():
            pos = line.find(symbol)
            rPos = line.rfind(symbol)
            if pos >= 0:
                if firstPos is None or pos < firstPos:
                    firstPos = pos
                    first = digit_or_word_value[symbol]
                if  lastPos is None or rPos > lastPos:
                    lastPos = rPos
                    last = digit_or_word_value[symbol]
        assert firstPos is not None and lastPos is not None
        sum += first * 10 + last
    return sum

def checkexamples():
    with open('example1.txt') as stream:
        result = part1(stream)
        print(f'example 1: {result}')
        assert result == 142, result

    with open('example2.txt') as stream:
        result = part2(stream)
        print(f'example 2: {result}')
        assert result == 281, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()