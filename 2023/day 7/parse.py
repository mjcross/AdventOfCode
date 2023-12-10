from cards import Hand, WildHand

def parse(stream):
    hands = []
    for rawline in stream:
        line=rawline.strip()

        handStr, bidStr = line.split()

        hand = Hand(handStr)
        hand.bid = int(bidStr)

        hands.append(hand)
    return hands

def parse2(stream):
    hands = []
    for rawline in stream:
        line=rawline.strip()

        handStr, bidStr = line.split()

        hand = WildHand(handStr)
        hand.bid = int(bidStr)

        hands.append(hand)
    return hands