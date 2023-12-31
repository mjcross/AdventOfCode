from module import parse, Pulse
from math import lcm

def getOutputs(inputs, modules):
    outputs = []
    for pulse in inputs:
        for module in modules.values():
            output = module.output(pulse)
            if output:
                outputs.append(output)
    return outputs


def part1(stream, nButtonPushes):
    modules = parse(stream)

    nLowPulses = 0
    nHighPulses = 0
    t = 0

    # push the button the required number of times
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
            inputs = getOutputs(inputs, modules)

    return nLowPulses * nHighPulses


def part2(stream, maxPeriod):
    modules = parse(stream)

    # find periods of inputs to the final conjunction module
    t = 0
    final = modules['mg']
    finalInputs = final.sources
    period = {fi: None for fi in finalInputs}

    for nPresses in range(1, maxPeriod):
        inputs = [Pulse(t, False, 'button', ['broadcaster'])]

        while inputs:
            t += 1
            inputs = getOutputs(inputs, modules)

            # check whether any of the final inputs went high
            if True in final.inputState.values():
                for fi in finalInputs:
                    if final.inputState[fi] == True and period[fi] is None:
                        print(f'\tperiod of {fi} is {nPresses}')
                        period[fi] = nPresses

    return lcm(*period.values())


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
        result = part1(stream, nButtonPushes=1_000)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream, maxPeriod=10_000)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()