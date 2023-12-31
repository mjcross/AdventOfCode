from dataclasses import dataclass
from collections import namedtuple


@dataclass
class Pulse:
    t: int
    level: bool
    source: str
    destinations: list[str]

    def __str__(self):
        if self.level == False:
            return f'{self.t:03d}\t{self.source} (LOW) -> {", ".join(self.destinations)}'
        else:
            return f'{self.t:03d}\t{self.source} (HIGH) -> {", ".join(self.destinations)}'

@dataclass
class Broadcaster:
    name: str
    destinations: list[str]

    def output(self, pulse: Pulse) -> list[Pulse]:
        if self.name in pulse.destinations:
            return Pulse(pulse.t + 1, pulse.level, self.name, self.destinations)
    

@dataclass
class Flipflop:
    name: str
    destinations: list[str]

    def __post_init__(self):
        self.state = False

    def output(self, pulse: Pulse) -> list[Pulse]:
        if self.name in pulse.destinations:
            if pulse.level == False:
                self.state = not(self.state)
                return Pulse(pulse.t + 1, self.state, self.name, self.destinations)


@dataclass
class Conjunction:
    name: str
    destinations: list[str]
    sources: list[str]

    def __post_init__(self):
        self.inputState = {s: False for s in self.sources}

    def output(self, pulse: Pulse) -> list[Pulse]:
        if self.name in pulse.destinations:
            self.inputState[pulse.source] = pulse.level
            if False in self.inputState.values():
                # send HIGH if any input is low
                return Pulse(pulse.t + 1, True, self.name, self.destinations)
            else:
                # send LOW if all inputs are high
                return Pulse(pulse.t + 1, False, self.name, self.destinations)
            

def parse(stream):
    rawlines = stream.readlines()
    lines = [rawline.strip() for rawline in rawlines]

    # first pass to identify connections
    Spec = namedtuple('Spec', 'prefix, name, dests')
    specs = []
    for line in lines:
        name, dest = line.split(' -> ')
        dests = dest.split(', ')
        if name == 'broadcaster':
            prefix = 'B'
        else:
            prefix = name[0]
            name = name[1:]

        specs.append(Spec(prefix, name, dests))

    # second pass to create modules
    modules = {}
    for spec in specs:
        if spec.prefix == 'B':
            modules[spec.name] = Broadcaster(spec.name, spec.dests)
        elif spec.prefix == '%':
            modules[spec.name] = Flipflop(spec.name, spec.dests)
        elif spec.prefix == '&':
            sources = [s.name for s in specs if spec.name in s.dests]
            modules[spec.name] = Conjunction(spec.name, spec.dests, sources)
        else:
            raise ValueError
        
    return modules