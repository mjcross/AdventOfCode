from collections import Counter
from enum import IntEnum

class Type(IntEnum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


class Card:
    ranks = [str(n) for n in range(2, 10)] + list('TJQKA')

    @property
    def strength(self):
        return self.rank + 2
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.rank = self.ranks.index(symbol)

    def __hash__(self):
        return self.rank

    def __str__(self):
        return self.symbol
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __gt__(self, other):
        return self.rank > other.rank
    

class Hand:
    @property
    def type(self):
        c = [c[1] for c in self.counts.most_common(2)]
        if c[0] == 5:
            return Type.FiveOfAKind
        elif c[0] == 4:
            return Type.FourOfAKind
        elif c == [3, 2]:
            return Type.FullHouse
        elif c[0] == 3:
            return Type.ThreeOfAKind
        elif c == [2, 2]:
            return Type.TwoPair
        elif c[0] == 2:
            return Type.OnePair
        else:
            return Type.HighCard

    def __init__(self, symbols):
        self.cards = [Card(symbol) for symbol in symbols]
        self.symbols = symbols
        self.counts = Counter(self)

    def __getitem__(self, index):
        return self.cards[index]

    def __repr__(self):
        return self.symbols
    
    def __gt__(self, other):
        if self.type.value > other.type.value:
            return True
        elif self.type.value < other.type.value:
            return False
        
        # compare hands of same type
        for selfCard, otherCard in zip(self.cards, other.cards):
            if selfCard > otherCard:
                return True
            elif otherCard > selfCard:
                return False
        else:
            return False
        

class WildCard(Card):
    ranks = list('J') + [str(n) for n in range(2, 10)] + list('TQKA')


class WildHand:

    def wildType(self):
        # replace Jacks with most common OTHER card
        counts = Counter(self.symbols).most_common(2)
        if counts[0][0] != 'J':
            wildSymbols = self.symbols.replace('J', counts[0][0])
        else:
            # most common card is Jack, choose next most common
            try:
                wildSymbols = self.symbols.replace('J', counts[1][0])    
            except(IndexError):
                # hand is 5 jacks so just leave alone
                wildSymbols = self.symbols
        # evaluate hand type with Jacks replaced
        counts = Counter(wildSymbols)
        c = [c[1] for c in counts.most_common(2)]
        if c[0] == 5:
            return Type.FiveOfAKind
        elif c[0] == 4:
            return Type.FourOfAKind
        elif c == [3, 2]:
            return Type.FullHouse
        elif c[0] == 3:
            return Type.ThreeOfAKind
        elif c == [2, 2]:
            return Type.TwoPair
        elif c[0] == 2:
            return Type.OnePair
        return Type.HighCard
    
    def __init__(self, symbols):
        self.cards = [WildCard(symbol) for symbol in symbols]
        self.symbols = symbols
        self.type = self.wildType()

    def __getitem__(self, index):
        return self.cards[index]

    def __repr__(self):
        return self.symbols
    
    def __gt__(self, other):
        if self.type.value > other.type.value:
            return True
        elif self.type.value < other.type.value:
            return False
        
        # compare hands of same type
        for selfCard, otherCard in zip(self.cards, other.cards):
            if selfCard > otherCard:
                return True
            elif otherCard > selfCard:
                return False
        else:
            return False


def main():
    # card comparisons
    assert Card('J') < Card('Q')
    assert Card('J') > Card('2')
    assert Card('2') < Card('J')

    # "Jacks Wild" card comparisons
    assert WildCard('J') < WildCard('Q')
    assert WildCard('J') < WildCard('2')
    assert WildCard('2') > WildCard('J')

    # hand comparisons
    assert Hand('AQT2Q').type == Type.OnePair
    assert Hand('AQTQA').type == Type.TwoPair
    assert Hand('AQQQT').type == Type .ThreeOfAKind
    assert Hand('AQAQA').type == Type.FullHouse
    assert Hand('QAAAA').type == Type.FourOfAKind
    assert Hand('AAAAA').type == Type.FiveOfAKind

    assert Hand('AQAQA') > Hand('2A333')    # full house beats three of a kind
    assert Hand('33332') > Hand('2AAAA')    # for hands of the same type, compare cards
    assert Hand('2AAAA') < Hand('33332')    # reverse rule

    assert Hand('KTTTT') > Hand('QQQQA')

if __name__ == '__main__':
    main()
