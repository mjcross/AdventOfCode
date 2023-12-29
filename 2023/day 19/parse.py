from  dataclasses import dataclass

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def score(self):
        return self.x + self.m + self.a + self.s


@dataclass
class Task:
    condition: str
    target: str


def parse(stream):

    # read workflows
    workflows = {}
    while True:
        line = stream.readline().strip()
        if not line:
            break

        key, taskSpec = line.split('{')
        assert taskSpec[-1] == '}'

        tasks = taskSpec.rstrip('}').split(',')
        tasks[-1] = 'True:' + tasks[-1]         # final task always runs

        workflows[key] = [Task(*task.split(':')) for task in tasks]
    
    # read parts
    parts = []
    while True:
        line = stream.readline().strip()
        if not line:
            break

        parts.append(eval('Part(' + line.strip('{}') + ')'))

    return workflows, parts