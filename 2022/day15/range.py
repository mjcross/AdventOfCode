class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __repr__(self):
        return f'Range(min={self.min:,}, max={self.max:,})'

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max

    def __len__(self):
        return self.max + 1  - self.min

    def overlaps(self, other):
        if self.max < other.min - 1:
            return False
        elif self.min > other.max + 1:
            return False
        else:
            return True

    def addtolist(self, list):
        if not list:
            return [self]
        else:
            newlist = []
            modifiedelements = []
            nooverlaps = True
            for other in list:
                if self == other:
                    newlist.append(other)       # new range duplicates existing one, so skip it
                    nooverlaps = False
                else:
                    if not self.overlaps(other):
                        newlist.append(other)   # existing range is disjoint so leave it alone
                    else:
                                                # new range overlaps existing: combine and add later (recursively)
                        combined = Range(min=min(self.min, other.min), max = max(self.max, other.max))
                        modifiedelements.append(combined)
                        #modifiedelements = combined.addtolist(modifiedelements)
                        nooverlaps = False

            if nooverlaps:
                newlist.append(self)            # new range is disjoint with everything so add it 

            for newelement in modifiedelements: # recursively add any new combined ranges
                newlist = newelement.addtolist(newlist)

            return newlist


def main():
    r1 = Range(2, 5)
    r2 = Range(7, 7)
    r3 = Range(9, 12)

    rangelist = [r1, r2, r3]
    print(Range(0, 11).addtolist(rangelist))

    

if __name__ == '__main__':
    main()