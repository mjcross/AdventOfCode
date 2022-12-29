from dataclasses import dataclass
from copy import copy

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
NONE = 4


@dataclass(frozen=True, eq=True)
class State:
    robots: tuple
    stock: tuple

    def __lt__(self, other):
        for material in (ORE, CLAY, OBSIDIAN, GEODE):
            if self.robots[material] > other.robots[material] or self.stock[material] > other.stock[material]:
                return False
        return True


def pathstr(path):
    code = list('ocBG.')
    repr = ''
    for item in path:
        repr += code[item]
    return repr


def parse(stream):
    blueprints = []
    for line in stream:
        robot_cost=[
            [   # ORE ROBOT COST
                int(line.split('ore robot costs')[1].split()[0]),
                0,
                0,
                0
            ],
            [   # CLAY ROBOT COST
                int(line.split('clay robot costs')[1].split()[0]),
                0,
                0,
                0
            ],
            [   # OBSIDIAN ROBOT COST
                int(line.split('obsidian robot costs')[1].split()[0]),
                int(line.split('obsidian robot costs')[1].split()[3]),
                0,
                0
            ],
            [   # GEODE ROBOT COST
                int(line.split('geode robot costs')[1].split()[0]),
                0,
                int(line.split('geode robot costs')[1].split()[3]),
                0
            ]
        ]
        blueprints.append(robot_cost)
    return blueprints



def can_make(new_robot, blueprint, state):
    for material in (ORE, CLAY, OBSIDIAN):
        if state.stock[material] < blueprint[new_robot][material]:
            return False
    return True


def make(new_robot, blueprint, state):
    if new_robot == NONE:
        return state
    else:
        new_stock = tuple(stock - cost for stock, cost in zip(state.stock, blueprint[new_robot]))
        new_robots = tuple(qty + int(index == new_robot) for index, qty in enumerate(state.robots))
        return State(robots=new_robots, stock=new_stock)


def do_production(state):
    robots = state.robots
    stock = tuple(stock + num_robots for stock, num_robots in zip(state.stock, state.robots))
    return State(robots=robots, stock=stock)


def remove_inferior(scenarios):
    cleaned = {}
    while scenarios:
        this_state, this_path = scenarios.popitem()
        for other_state in scenarios.keys():
            if this_state < other_state:
                break
        else:
            cleaned[this_state] = this_path
    return cleaned


def most_geodes(blueprint, maxclean, maxpath):

    # fastest possible consumption rates with this blueprint
    max_consumption_rate = [
        max([blueprint[robot][ORE] for robot in [CLAY, OBSIDIAN, GEODE]]),
        max([blueprint[robot][CLAY] for robot in [OBSIDIAN, GEODE]]),
        blueprint[GEODE][OBSIDIAN]
    ]

    scenarios = {State(robots=(1,0,0,0), stock=(0,0,0,0)): tuple()}
    pathlen = 0
    print('\t', end='')
    while pathlen < maxpath:   # no point making any new robots on the last turn
        print(f'{pathlen}:{len(scenarios)}', end=' ', flush=True)
        pathlen += 1
        new_scenarios = {}
        for state, path in scenarios.items():

            # decide what to make (not worth making anything on the final turn)
            if pathlen != maxpath:
                for robot in [OBSIDIAN, CLAY, ORE]:
                    
                    # stock level at the start of the penultimate round
                    final_stock = state.stock[robot] + (maxpath - pathlen - 1) * (state.robots[robot] - max_consumption_rate[robot])

                    if final_stock < 0 and can_make(robot, blueprint, state):
                        new_state = make(robot, blueprint, do_production(state))
                        new_scenarios[new_state] = path + (robot,)

            # in the 'base' scenario, make a GEODE robot if we can, otherwise do nothing
            if can_make(GEODE, blueprint, state):
                robot = GEODE
            else:
                robot = NONE
            new_state = make(robot, blueprint, do_production(state))
            new_scenarios[new_state] = path + (robot,)

        # remove inferior scenarios (a relatively expensive process)
        if len(new_scenarios) < maxclean:
            scenarios = remove_inferior(new_scenarios)
        else:
            scenarios = new_scenarios
        
    print()
    return max([scenario.stock[GEODE] for scenario in scenarios])


def part1(blueprints):
    score = 0
    for blueprint_num, blueprint in enumerate(blueprints, start=1):
        print(f'Blueprint {blueprint_num}')
        max_opened = most_geodes(blueprint, maxclean=10_000, maxpath=24)
        print(f'\t{max_opened} geodes')
        score += blueprint_num * max_opened
    return score


def part2(blueprints):
    score = 1
    for blueprint_num, blueprint in enumerate(blueprints, start=1):
        print(f'Blueprint {blueprint_num}')
        max_opened = most_geodes(blueprint, maxclean=10_000_000, maxpath=32)
        score *= max_opened
    return score


def checkexamples():
    with open('example.txt') as stream:
        blueprints = parse(stream)
        example1 = part1(blueprints)
        print(f'>>> example1 score: {example1} <<<\n')
        assert example1 == 33

        #! takes forever...
        #example2 = part2(blueprints[:3])
        #print(f'>>> example1 score: {example1} <<<\n')
        #assert example2 == 56 * 62


def main():

    checkexamples()

    print()
    with open('input.txt') as stream:
        blueprints = parse(stream)
        score = part1(blueprints)
        print(f'>>> PART 1: {score} <<<\n')

    with open('input.txt') as stream:
        blueprints = parse(stream)
        score = part2(blueprints[:3])
        print(f'>>> PART 2: {score} <<<\n')

if __name__ == '__main__':
    main()