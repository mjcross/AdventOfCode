from dataclasses import dataclass
from parse import parse
from copy import deepcopy

def part1(stream):
    workflows, parts = parse(stream)
    accepted = []
    rejected = []
    for part in parts:
        x = part.x
        m = part.m
        a = part.a
        s = part.s
        
        workflowName = 'in'     # always start with the 'in' workflow
        while True:
            for task in workflows[workflowName]:
                if (eval(task.condition)):
                    workflowName = task.target
                    break

            if workflowName == 'A':
                accepted.append(part)
                break
            elif workflowName == 'R':
                rejected.append(part)
                break

    return sum([part.score for part in accepted])
    

@dataclass
class Span:
    first: int
    last: int

    def __repr__(self):
        return f'[{self.first}-{self.last}]'
    
    def __len__(self):
        return self.last - self.first + 1


@dataclass
class Part:
    workflowName: str
    x: Span
    m: Span
    a: Span
    s: Span

    def numCombinations(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)


def part2(stream):
    workflows, _ = parse(stream)

    accepted = []
    parts = [Part(workflowName='in',
                  x=Span(1, 4000), 
                  m=Span(1, 4000), 
                  a=Span(1, 4000), 
                  s=Span(1, 4000))]

    while parts:
        part = parts.pop()
        
        if part.workflowName == 'A':
            accepted.append(part)
            continue

        elif part.workflowName == 'R':
            continue

        workflow = workflows[part.workflowName]
        
        try:
            for task in workflow:
                conditionStr = task.condition

                if conditionStr == 'True':
                    part.workflowName = task.target
                    parts.append(part)
                    raise StopIteration

                condVarName = conditionStr[0]
                condOp = conditionStr[1]
                condVal = int(conditionStr[2:])

                span = part.__getattribute__(condVarName)

                if condOp == '>':
                    if span.first > condVal:
                        # full pass
                        part.workflowName = task.target
                        parts.append(part)
                        raise StopIteration
                    if span.last <= condVal:
                        # full fail
                        continue    # carry on to next task in workflow

                    # the condition splits the span

                    # the passing fraction branches to a different workflow
                    passPart = deepcopy(part)
                    passPart.__setattr__(condVarName, Span(condVal + 1, span.last))
                    passPart.workflowName = task.target
                    parts.append(passPart)

                    # the failing fraction carries on to the next task in the workflow  
                    part.__setattr__(condVarName, Span(span.first, condVal))
                    continue    # carry on to next task in workflow

                if condOp == '<':
                    if span.last < condVal:
                        # full pass
                        part.workflowName = task.target
                        parts.append(part)
                        raise StopIteration
                    if span.first >= condVal:
                        # full fail
                        continue    # carry on to next task in workflow

                    # the condition splits the span

                    # the passing fraction branches to a different workflow
                    passPart = deepcopy(part)
                    passPart.__setattr__(condVarName, Span(span.first, condVal - 1))
                    passPart.workflowName = task.target
                    parts.append(passPart)

                    # the failing fraction carries on to the next task in the workflow  
                    part.__setattr__(condVarName, Span(condVal, span.last))
                    continue    # carry on to next task in workflow    

        except StopIteration:
            pass

    return sum([part.numCombinations() for part in accepted])
            

def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 19114, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 167409079868000, result


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