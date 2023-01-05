snafu_numeral = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2
}

numeral_snafu = {
    0: '0',
    1: '1',
    2: '2',
    -1: '-',
    -2: '='
}

def snafu_to_decimal(snafu_str):
    snafu_list = list(snafu_str)
    column_val = 1
    decimal = 0
    while snafu_list:
        decimal += column_val * snafu_numeral[snafu_list.pop()]
        column_val *= 5
    return decimal


biggest_snafu = {
    num_digits: snafu_to_decimal(num_digits * '2') for num_digits in range(1, 50)
}


def decimal_to_snafu(num):
    # get the biggest column value needed
    for num_digits in range(1, 50):
        if biggest_snafu[num_digits] >= num:
            break
    else:
        raise ValueError('number too big')
    column_val = 5 ** (num_digits - 1)

    #print(f'{num} needs {num_digits} digits, highest column value {column_val}')

    snafu_str = ''
    while column_val > 1:

        # calculate digit
        for digit in (2, 1, 0, -1, -2):
            digit_val = digit * column_val
            remainder = num - digit_val

            #print(f'\t{num} - {digit} * {column_val} gives remainder {remainder}')
            if abs(remainder) <= biggest_snafu[num_digits - 1]:
                #print()
                break
        else:
            raise ValueError

        # next column
        snafu_str += numeral_snafu[digit]
        num = remainder

        column_val //= 5
        num_digits -= 1
    
    # final digit
    snafu_str += numeral_snafu[num]

    return snafu_str


def part1(stream):
    numbers = [snafu_to_decimal(line.rstrip()) for line in stream]
    return decimal_to_snafu(sum(numbers))


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == '2=-1=0', result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    #with open('input.txt') as stream:
    #    result = part2(stream)
    #    print(f'part2 {result}')


if __name__ == '__main__':
    main()