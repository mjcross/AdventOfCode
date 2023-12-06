from card import Card

def parse(stream):
    cardList = []
    for rawline in stream:
        line = rawline.strip()

        # extract top level fields
        cardField, numsField = line.split(':')
        
        # parse card number
        fieldName, cardNumStr = cardField.split()
        assert fieldName == 'Card'
        cardNum = int(cardNumStr)

        # extract winning numbers and game numbers
        winningNumsField, gameNumsField = numsField.split('|')

        # parse winning numbers and game numbers
        winningNums = [int(s) for s in winningNumsField.split()]
        gameNums = [int(s) for s in gameNumsField.split()]

        # create and add card object
        cardList.append(Card(cardNum, winningNums, gameNums))

    return cardList