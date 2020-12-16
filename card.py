"""
    This file contains the card class used for the blackjack game. 
"""

from constants import cardRank, cardFigure


class Card:
    def __init__(self, rank, figure):
        self.rank = rank
        self.figure = figure

    def __str__(self):
        return(cardRank[self.rank] + " de " + cardFigure[self.figure])

    def getCardFile(self):
        return "./assets/cards/" + cardRank[self.rank] + \
            " de " + cardFigure[self.figure] + ".PNG"

    def getRank(self):
        return(self.rank)

    def getFigure(self):
        return(self.figure)

    def getCardValue(self):
        """
            get card value: 
                rank < 10 => value = rank
                rank >= 10 => value = 10;
        """
        if self.rank > 9:
            return(10)
        else:
            return(self.rank)
