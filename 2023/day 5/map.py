from dataclasses import dataclass, field

@dataclass
class Span:
    start: int
    stop: int


@dataclass
class Mapping:
    destStart: int
    srcStart: int
    rangeLen: int

    @property
    def destRange(self):
        return range(self.destStart, self.destStart + self.rangeLen)
    
    @property
    def srcRange(self):
        return range(self.srcStart, self.srcStart + self.rangeLen)
    
    @property
    def srcStop(self):
        return self.srcStart + self.rangeLen - 1
    
    @property
    def destStop(self):
        return self.destStart + self.rangeLen - 1
    
    def map(self, source):
        if source in self.srcRange:
            offset = source - self.srcStart
            return self.destStart + offset
        else:
            return source

    def mapSpan(self, span):
        newSpans = []
        if span.start < self.srcStart:
            # unmapped leading part
            leaderStart = span.start
            leaderStop = min(span.stop, self.srcStart - 1)
            newSpans.append(Span(leaderStart, leaderStop))    
        if span.stop > self.srcStop:
            # unmapped trailing part
            trailerStop = span.stop
            trailerStart = max(span.start, self.srcStop + 1)
            newSpans.append(Span(trailerStart, trailerStop))
        overlapStart = max(self.srcStart, span.start)
        overlapStop = min(self.srcStop, span.stop)
        if overlapStart <= span.stop and overlapStop >= span.start:
            # mapped overlapping part
            newSpans.append(Span(self.map(overlapStart), self.map(overlapStop)))
        return newSpans

@dataclass
class Map:
    mappings: list[Mapping] = field(default_factory=list)

    def map(self, source):
        for mapping in self.mappings:
            mappedSource = mapping.map(source)
            if mappedSource != source:
                return mappedSource
        return source
        
    def mapSpans(self, spans):
        newSpans = []
        for span in spans:
            for mapping in self.mappings:
                newSpans += mapping.mapSpan(span)
        return newSpans
    


def main():
    # test Mapping.mapSpan()
    mapping = Mapping(srcStart=10, destStart=100, rangeLen=10)  # {10...19} -> {100...119}

    # check all the different overlaps and edge cases
    assert mapping.mapSpan(Span(5, 5)) == [Span(5, 5)]
    assert mapping.mapSpan(Span(5, 9)) == [Span(5, 9)]
    assert mapping.mapSpan(Span(5, 10)) == [Span(5, 9), Span(100, 100)]
    assert mapping.mapSpan(Span(5, 15)) == [Span(5, 9), Span(100, 105)]
    assert mapping.mapSpan(Span(5, 19)) == [Span(5, 9), Span(100, 109)]
    assert mapping.mapSpan(Span(5, 19)) == [Span(5, 9), Span(100, 109)]
    assert mapping.mapSpan(Span(10, 19)) == [Span(100, 109)]
    assert mapping.mapSpan(Span(12, 17)) == [Span(102, 107)]
    assert mapping.mapSpan(Span(15, 25)) == [Span(20, 25), Span(105, 109)]
    assert mapping.mapSpan(Span(19, 25)) == [Span(20, 25), Span(109, 109)]
    assert mapping.mapSpan(Span(20, 25)) == [Span(20, 25)]
    assert mapping.mapSpan(Span(25, 30)) == [Span(25, 30)]
    assert mapping.mapSpan(Span(10, 19)) == [Span(100, 109)]
    assert mapping.mapSpan(Span(9, 20)) == [Span(9, 9), Span(20, 20), Span(100, 109)]
    assert mapping.mapSpan(Span(5, 25)) == [Span(5, 9), Span(20, 25), Span(100, 109)]

if __name__ == '__main__':
    main()