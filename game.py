from random import shuffle
from scores import *
from constants import cardRank, cardFigure
from card import Card
from hand import Hand


class Game:
    def __init__(self):

        self.deck = []
        self.pit = []

        # initialize the deck
        self.resetDeck()

        self.dealerHand = Hand()
        self.playerHand = Hand()
        self.scores = getScoresFromFile()

    def resetDeck(self):
        for figure in cardFigure:
            for rank in range(1, len(cardRank) + 1):
                self.deck.append(Card(rank, figure))

        shuffle(self.deck)

    def resetHands(self):
        self.dealerHand = Hand()
        self.playerHand = Hand()

    def initializeGameScore(self):
        self.scores['player'] = 0
        self.scores['dealer'] = 0

    def getScores(self):
        return sortScores(self.scores)

    def updateScoreDealer(self):
        self.scores['dealer'] += 1

    def updateScorePlayer(self):
        self.scores['player'] += 1

    def dealerTurn(self):
        if (len(self.deck) == 0):
            self.resetDeck()
        card = self.deck.pop(0)
        self.dealerHand.addCard(card)

    def playerTurn(self):
        if (len(self.deck) == 0):
            self.resetDeck()
        card = self.deck.pop(0)
        self.playerHand.addCard(card)

    def saveGameScore(self):
        saveScores(self.scores)

    def encodeDeck(self):
        code = [0] * 52
        for card in self.deck:
            if card.figure == "p":
                fig = 0
            elif card.figure == "t":
                fig = 1
            elif card.figure == "c":
                fig = 2
            else:
                fig = 3

            code[4 * (card.rank-1) + fig] = 1

        return code
