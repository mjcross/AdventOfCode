from module import parse, Pulse

def part1(stream, nButtonPushes):
    modules = parse(stream)

    nLowPulses = 0
    nHighPulses = 0
    t = 0

    # push the button four times
    for _ in range(nButtonPushes):
        # send a 'LOW' pulse to the broadcaster
        inputs = [Pulse(t, False, 'button', ['broadcaster'])]

        # let everything stabilise
        while inputs:
            
            # count high and low pulses
            for pulse in inputs:
                if pulse.level == True:
                    nHighPulses += len(pulse.destinations)
                else:
                    nLowPulses += len(pulse.destinations)

            # collect ouput pulses
            outputs = []
            t += 1
            for pulse in inputs:
                for module in modules:
                    output = module.output(pulse)
                    if output:
                        outputs.append(output)
            inputs = outputs

    return nLowPulses * nHighPulses


def part2(stream, nButtonPushes):
    modules = parse(stream)

    t = 0

    # push the button four times
    for buttonPressNum in range(nButtonPushes):
        # send a 'LOW' pulse to the broadcaster
        inputs = [Pulse(t, False, 'button', ['broadcaster'])]

        # let everything stabilise
        while inputs:
            
            for pulse in inputs:
                if pulse.level == False and 'rx' in pulse.destinations:
                    return buttonPressNum

            # collect ouput pulses
            outputs = []
            t += 1
            for pulse in inputs:
                for module in modules:
                    output = module.output(pulse)
                    if output:
                        outputs.append(output)
            inputs = outputs



def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream, nButtonPushes=1000)
        print(f'example1: {result}')
        assert result == 11687500, result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream, nButtonPushes=1000)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream, 1000000)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()