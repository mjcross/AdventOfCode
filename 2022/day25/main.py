snafu_sum = {
    ('=', '='): ('-', '1'), ('=', '-'): ('-', '2'), ('=', '0'): ('0', '='), ('=', '1'): ('0', '-'), ('=', '2'): ('0', '0'),
    ('-', '='): ('-', '2'), ('-', '-'): ('0', '='), ('-', '0'): ('0', '-'), ('-', '1'): ('0', '0'), ('-', '2'): ('0', '1'),
    ('0', '='): ('0', '='), ('0', '-'): ('0', '-'), ('0', '0'): ('0', '0'), ('0', '1'): ('0', '1'), ('0', '2'): ('0', '2'),
    ('1', '='): ('0', '-'), ('1', '-'): ('0', '0'), ('1', '0'): ('0', '1'), ('1', '1'): ('0', '2'), ('1', '2'): ('1', '='), 
    ('2', '='): ('0', '0'), ('2', '-'): ('0', '1'), ('2', '0'): ('0', '2'), ('2', '1'): ('1', '='), ('2', '2'): ('1', '-')
}


def snafu_add(s1, s2):
    # pad numbers to same length with leading zeros
    s1 = s1.rjust(len(s2), '0')
    s2 = s2.rjust(len(s1), '0')

    sum = ''
    carry = '0'
    for d1, d2 in reversed(list(zip(s1, s2))):
        carry_digit, sum_digit = snafu_sum[d1, d2]
        sum = sum_digit + sum
        carry = carry_digit + carry

    # trim leading zeroes 
    carry = carry.lstrip('0')
    sum = sum.lstrip('0')

    # recurse until there's no carry
    if carry:
        return snafu_add(carry, sum)
    else:
        return carry, sum


def main():
    """ improved solution that performs the addition in 'native' snafu """
    with open('input.txt') as stream:
        total = '0'
        for line in stream:
            snafu_num = line.rstrip()
            result = snafu_add(total, snafu_num)[1]
            total = result
        print(total)

if __name__ == '__main__':
    main()