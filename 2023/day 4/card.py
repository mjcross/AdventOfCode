from dataclasses import dataclass, field

@dataclass
class Card:
    num: int
    winningNums: list[int] = field(default_factory=list)
    gameNums: list[int] = field(default_factory=list)
    score: int = 0

    @property
    def getScore(self):
        cardScore = 0
        matchValue = 1
        for gameNum in self.gameNums:
            if gameNum in self.winningNums:
                cardScore = matchValue
                matchValue *= 2
                #! print("card", self.num, gameNum, "score", cardScore)
        return cardScore
    
    @property
    def numMatches(self):
        matchCount = 0
        for gameNum in self.gameNums:
            if gameNum in self.winningNums:
                matchCount += 1
        return matchCount
    
    @property
    def copies(self):
        cardNums = []
        #! print("card", self.num, "no. matches:", self.numMatches, self.winningNums, self.gameNums)
        for i in range(self.numMatches):
            cardNums.append(self.num + 1 + i)
        return cardNums