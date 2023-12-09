from dataclasses import dataclass, field

@dataclass
class Race:
    time: int
    distance: int

def parse(stream):
    times = []
    distances = []
    for rawline in stream:
        line = rawline.strip()
        keyword, contents = line.split(':')
        if keyword == 'Time':
            times = map(int, contents.split())
        elif keyword == 'Distance':
            distances = map(int, contents.split())
        else:
            raise(ValueError)
    return [Race(*tuple) for tuple in zip(times, distances)]

def parse2(stream):
    races = parse(stream)
    timeStr = ''
    distanceStr = ''
    for race in races:
        timeStr += str(race.time)
        distanceStr += str(race.distance)
    return int(timeStr), int(distanceStr)