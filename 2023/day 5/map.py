from dataclasses import dataclass, field

@dataclass
class Span:
    start: int
    stop: int

    def __repr__(self):
        return f'{self.start}-{self.stop}'


@dataclass
class Mapping:
    destStart: int
    srcStart: int
    rangeLen: int

    def __repr__(self):
        return f'{self.srcStart}-{self.srcStop} -> {self.destStart}-{self.destStop}'

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
        leader = None
        if span.start < self.srcStart:
            # unmapped leading part
            leaderStart = span.start
            leaderStop = min(span.stop, self.srcStart - 1)
            leader = Span(leaderStart, leaderStop)

        trailer = None
        if span.stop > self.srcStop:
            # unmapped trailing part
            trailerStop = span.stop
            trailerStart = max(span.start, self.srcStop + 1)
            trailer = Span(trailerStart, trailerStop)

        overlap = None
        overlapStart = max(self.srcStart, span.start)
        overlapStop = min(self.srcStop, span.stop)
        if overlapStart <= span.stop and overlapStop >= span.start:
            # mapped overlapping part
            overlap = Span(self.map(overlapStart), self.map(overlapStop))

        mapped = None
        unmapped = []
        if leader:
            unmapped.append(leader)
        if trailer:
            unmapped.append(trailer)
        if overlap:
            mapped = overlap
        return (unmapped, mapped)


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
        mappedSpans = []
        for mapping in self.mappings:
            unmappedSpans = []   # unmapped spans for the next mapping
            for span in spans:
                unmapped, mapped = mapping.mapSpan(span)
                if unmapped:
                    unmappedSpans += unmapped
                if mapped:
                    mappedSpans.append(mapped)
            spans = unmappedSpans
        return mappedSpans + unmappedSpans


def main():
    # test Mapping.mapSpan()
    mapping = Mapping(srcStart=10, destStart=100, rangeLen=10)  # {10...19} -> {100...119}

    # check all the different overlaps and edge cases
    # the fields are ([leader, trailer], overlap)
    assert mapping.mapSpan(Span(5, 5)) == ([Span(5, 5)], None)
    assert mapping.mapSpan(Span(5, 9)) == ([Span(5, 9)], None)
    assert mapping.mapSpan(Span(5, 10)) == ([Span(5, 9)], Span(100, 100))
    assert mapping.mapSpan(Span(5, 15)) == ([Span(5, 9)], Span(100, 105))
    assert mapping.mapSpan(Span(5, 19)) == ([Span(5, 9)], Span(100, 109))
    assert mapping.mapSpan(Span(10, 19)) == ([], Span(100, 109))
    assert mapping.mapSpan(Span(12, 17)) == ([],Span(102, 107))
    assert mapping.mapSpan(Span(15, 25)) == ([Span(20, 25)], Span(105, 109))
    assert mapping.mapSpan(Span(19, 25)) == ([Span(20, 25)], Span(109, 109))
    assert mapping.mapSpan(Span(20, 25)) == ([Span(20, 25)], None)
    assert mapping.mapSpan(Span(25, 30)) == ([Span(25, 30)], None)
    assert mapping.mapSpan(Span(10, 19)) == ([], Span(100, 109))
    assert mapping.mapSpan(Span(9, 20)) == ([Span(9, 9), Span(20, 20)], Span(100, 109))
    assert mapping.mapSpan(Span(5, 25)) == ([Span(5, 9), Span(20, 25)], Span(100, 109))

if __name__ == '__main__':
    main()