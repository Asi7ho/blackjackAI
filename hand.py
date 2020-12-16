"""
    This file contains the hand class used for the blackjack game. 
"""


class Hand:
    def __init__(self):
        self.hand = []

    def addCard(self, card):
        self.hand.append(card)

    def handValue(self):
        handValue = 0
        # Compute hand value
        for card in self.hand:
            handValue += card.getCardValue()

        # Compute the Ace value: Ace card could be 1 or 11
        for card in self.hand:
            if card.getRank() == 1 and handValue + 10 <= 21:
                handValue += 10

        return(handValue)

    def addCard(self, card):
        self.hand.append(card)

    def getLastCard(self):
        return self.hand[-1]
