from enum import Enum, auto
from copy import copy

class Robot(Enum):
    NONE = auto()
    ORE = auto()
    CLAY = auto()

    def __repr__(self):
        return self.name[0]


class Factory:
    def __init__(self,
                 timeleft=0,
                 ore_rate=0,
                 clay_rate=0,
                 ore_stock=0,
                 clay_stock=0,
                 path=[]):
        self.timeleft = timeleft
        self.ore_rate = ore_rate
        self.ore_stock = ore_stock
        self.clay_rate = clay_rate
        self.clay_stock = clay_stock
        self.path = copy(path)
        self.best_clay = 0
        self.best_clay_path = []
        self.best_ore = 0
        self.best_ore_path = []

    def __repr__(self):
        repr = (f'timeleft={self.timeleft}, '
            f'ore_rate={self.ore_rate}, clay_rate={self.clay_rate}, '
            f'ore_stock={self.ore_stock}, clay_stock={self.clay_stock}, '
            f'path={self.path}')
        return repr

    def copy(self):
        return Factory(self.timeleft, self.ore_rate, self.clay_rate, self.ore_stock, self.clay_stock, self.path)

    def make(self, robot):
        self.path.append(robot)

        # production from existing robots
        self.ore_stock += self.ore_rate
        self.clay_stock += self.clay_rate
        self.timeleft -= 1
        if self.timeleft == 0:
            # finished the path
            #print(f'{self.path} ore {self.ore_stock} clay {self.clay_stock}')
            return self.clay_stock, self.path

        # create new robot
        if robot is Robot.ORE:
            self.ore_stock -= 4
            self.ore_rate += 1
        elif robot is Robot.CLAY:
            self.ore_stock -= 2
            self.clay_rate += 1
        else:
            assert robot is Robot.NONE

        # recurse through all the different things we could do next

        # 'do nothing' option is always available
        best_clay, best_path = self.copy().make(Robot.NONE)

        # if we have enough stock and enough time, try making a clay robot
        if self.ore_stock >= 2 and self.timeleft >= 2:
            clay, path = self.copy().make(Robot.CLAY)
            if clay > best_clay:
                best_clay, best_path = clay, path

        # if we have enough stock and enough time, try making an ore robot
        if self.ore_stock >= 4 and self.timeleft >= 2:
            clay, path = self.copy().make(Robot.ORE)
            if clay > best_clay:
                best_clay, best_path = clay, path

        return best_clay, best_path


def main():
    """
    This is an experiment looking at just the Ore and Clay robots from the first blueprint:
        Ore robot costs 4 ore
        Clay robot costs 2 ore
    The results are quite interesting. 
    
    For path lengths up to and including 17 it is not worth the delay to build a second ore 
    robot, so with the output of a single one the factory runs at half capacity:
        Most clay 56, from path [N, N, C, N, C, N, C, N, C, N, C, N, C, N, C, N, N]
    
    For longer path lengths 18 or more it is worth making a second ore robot so that the
    factory runs at full capacity:
        Most clay 66, from path [N, N, N, N, N, O, C, C, C, C, C, C, C, C, C, C, C, N]

    Note 1) With the current parameters it's never worth building a third ore robot because
            the factory is already at full capacity.   
         2) In this case would be straightforward to work out the path length at which it is
            worth building the second ore robot, and also the number of ore robots required 
            to fully utilise the factory. Presumably if that were a fractional number then
            it might *eventually* be worth building the next higher integer number. 
         3) In all the cases examined so far ithe optimum approach seems to be to build all 
            the ore robots first, before starting to build clay robots. Is this an artifact 
            of the cost parameters?

    """
    factory = Factory(timeleft=17,
                      ore_rate=1,
                      ore_stock=0,
                      clay_rate=0,
                      clay_stock=0,
                      path=[])
    bestclay, bestpath = factory.make(Robot.NONE)
    print(f'Most clay {bestclay}, from path {bestpath}')


if __name__ == '__main__':
    main()