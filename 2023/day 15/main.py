def hash_val(s):
    x = 0
    for c in s:
        i = ord(c)
        x += i
        x = (17 * x) % 256
    return x


def part1(stream):
    rawline = stream.readline()
    fields = rawline.strip().split(',')
    total = 0
    for field in fields:
        total += hash_val(field)
    return total


def part2(stream):
    boxes = [{} for _ in range(256)]
    rawline = stream.readline()
    fields = rawline.strip().split(',')
    total = 0
    for field in fields:
        if '-' in field:
            operation = '-'
            focal_length = None
            label = field.rstrip('-')
        elif '=' in field:
            operation = '='
            label, focal_length_str = field.split('=')
            focal_length = int(focal_length_str)
        else:
            raise ValueError(f'invalid operation: {field}')
        box = boxes[hash_val(label)]

        if operation == '-':
            if label in box:
                del box[label]

        elif operation == '=':
            box[label] = focal_length

    total = 0
    for boxNum, box in enumerate(boxes):
        if box:
            for slotNum, focal_length in enumerate(box.values()):
                total += (boxNum + 1) * (slotNum + 1) * focal_length
    return total

def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result ==1320, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 145, result


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