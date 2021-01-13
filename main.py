import sys

from ai import Dqn
import numpy as np
from game import Game
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

WINDOW_WIDTH = 1136
WINDOW_HEIGHT = 850
CARD_WIDTH = 167
CARD_HEIGHT = 225

brain = Dqn(3, 2, 0.9)
action = [1, 0]
last_reward = 0
scores = []

buttonStyle = """
                QPushButton {
                    font-size: 26px;
                    width: 100px;
                    border-radius: 10px;
                    border-style: outset;
                    background: white;
                    padding: 5px;
                }

                QPushButton:hover {
                    background: qradialgradient(
                        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                        radius: 1.35, stop: 0 #fff, stop: 1 #bbb
                    );
                }
              """


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.game = Game()

        self.username = "unknown"
        self.lineEdit = QLineEdit()

        self.cardsDealt = False
        self.exitGame = False

        # window
        self.setWindowTitle("Black Jack ++")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # launch
        self.homePage()
        self.show()
        self.status = 0

    def homePage(self):
        # add buttons for home page
        loadButton = QPushButton("Load")
        loadButton.setStyleSheet(buttonStyle)
        loadButton.clicked.connect(self.loadModel)

        rulesButton = QPushButton("Rules")
        rulesButton.setStyleSheet(buttonStyle)
        rulesButton.clicked.connect(self.rulesPage)

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox.addWidget(loadButton)
        hbox.addWidget(rulesButton)

        widget = QWidget()

        # set the background image as the home page
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        background.setStyleSheet(
            "background-image: url(./assets/backgrounds/fond_acceuil.png)")

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def rulesPage(self):
        # add buttons for rules page
        playButton = QPushButton("Play")
        playButton.setStyleSheet(buttonStyle)
        playButton.clicked.connect(self.handleGame)

        backButton = QPushButton("Back")
        backButton.setStyleSheet(buttonStyle)
        backButton.clicked.connect(self.homePage)

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox.addWidget(playButton)
        hbox.addWidget(backButton)

        widget = QWidget()

        # set the background image as the rules page
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        background.setStyleSheet(
            "background-image: url(./assets/backgrounds/fond regle.PNG)")

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.game.initializeGameScore()

    def gamePage(self):

        global brain
        global last_reward
        global scores

        # add buttons for game page
        leaveButton = QPushButton("Leave")
        leaveButton.setStyleSheet(buttonStyle)
        leaveButton.clicked.connect(self.leavePage)

        # add players name
        labelDealer = QLabel("Dealer: {}".format(
            self.game.dealerHand.handValue()))
        labelDealer.setFont(QFont('Arial', 26))
        labelDealer.setStyleSheet(
            "padding:5px 20px; color: white; background-color:rgb(43, 43, 43); border-radius:20px")

        # add number of dealer victory
        DealerWin = QLabel("Victory: {}".format(self.game.scores['dealer']))
        DealerWin.setFont(QFont('Arial', 26))
        DealerWin.setStyleSheet(
            "padding:5px 20px; color: white; background-color:rgb(43, 43, 43); border-radius:20px")

        # add player name
        labelPlayer = QLabel("You: {}".format(
            self.game.playerHand.handValue()))
        labelPlayer.setFont(QFont('Arial', 26))
        labelPlayer.setStyleSheet(
            "padding:5px 20px; color: white; background-color:rgb(43, 43, 43); border-radius:20px")

        # add number of player victory
        PlayerWin = QLabel("Victory: {} ({:.2f})".format(
            self.game.scores['player'], self.game.scores['player'] / (self.game.scores['player'] + self.game.scores['dealer'] + 2e-16)))
        PlayerWin.setFont(QFont('Arial', 26))
        PlayerWin.setStyleSheet(
            "padding:5px 20px; color: white; background-color:rgb(43, 43, 43); border-radius:20px")

        # add ai score
        AIScore = QLabel("AI Score: {:.3f}".format(brain.score()))
        AIScore.setFont(QFont('Arial', 26))
        AIScore.setStyleSheet(
            "padding:5px 20px; color: white; background-color:rgb(43, 43, 43); border-radius:20px")

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)

        # add widgets
        wrapperGameV = QVBoxLayout()
        wrapperGameH = QHBoxLayout()
        wrapperGameH2 = QHBoxLayout()

        # label Dealer
        wrapperGameH.addWidget(labelDealer, alignment=Qt.AlignCenter)
        wrapperGameH.addWidget(DealerWin, alignment=Qt.AlignCenter)
        wrapperGameV.addLayout(wrapperGameH)

        # label player
        wrapperGameV.addStretch()
        wrapperGameH2.addWidget(labelPlayer, alignment=Qt.AlignCenter)
        wrapperGameH2.addWidget(PlayerWin, alignment=Qt.AlignCenter)
        wrapperGameH2.addWidget(AIScore, alignment=Qt.AlignCenter)
        wrapperGameV.addLayout(wrapperGameH2)

        vbox.addLayout(wrapperGameV)
        vbox.addLayout(hbox)

        hbox.addWidget(leaveButton)

        widget = self.updateGamePage()

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        return

    def playHand(self):
        if self.cardsDealt:

            win = self.checkWin()

            if win:
                self.game.resetHands()
                self.status = 0
                return 1

            playerState = self.game.playerHand.handValue()

            dealerState = self.game.dealerHand.handValue()

            AceState = 0
            for card in self.game.playerHand.hand:
                if card.getRank() == 1 and playerState + 10 <= 21:
                    AceState = 1

            last_signal = (
                (np.array([playerState, dealerState, AceState])).T).tolist()
            action2take = brain.update(last_reward, last_signal)
            scores.append(brain.score())

            if action2take == 0:
                self.hitEvent()
            else:
                self.standEvent()

    def checkWin(self):
        global last_reward

        if self.game.dealerHand.handValue() == 21 and len(self.game.dealerHand.hand) == 2:
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec_()
            self.cardsDealt = False
            last_reward = -1
            self.lost()
            return 1

        if self.game.playerHand.handValue() == 21 and len(self.game.playerHand.hand) == 2:
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec_()
            self.cardsDealt = False
            last_reward = 1
            self.win()
            return 1

        if self.game.playerHand.handValue() > 21:
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec_()
            self.cardsDealt = False
            last_reward = -1
            self.lost()
            return 1

        if self.game.dealerHand.handValue() > 21:
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec_()
            self.cardsDealt = False
            last_reward = 1
            self.win()
            return 1

        if self.status == 1:
            if self.game.dealerHand.handValue() >= self.game.playerHand.handValue():
                loop = QEventLoop()
                QTimer.singleShot(100, loop.quit)
                loop.exec_()
                self.cardsDealt = False
                last_reward = -1
                self.lost()
                return 1

    def handleGame(self):
        while not self.exitGame:
            self.processGame()

    def processGame(self):
        if not self.exitGame:
            self.gamePage()

        # game
        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)
        loop.exec_()
        self.game.dealerTurn()
        if not self.exitGame:
            self.gamePage()

        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)
        loop.exec_()
        self.game.playerTurn()
        if not self.exitGame:
            self.gamePage()

        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)
        loop.exec_()
        self.game.playerTurn()
        if not self.exitGame:
            self.gamePage()

        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)
        loop.exec_()
        self.cardsDealt = True
        if not self.exitGame:
            self.gamePage()

        stop = 0
        while not stop:
            stop = self.playHand()

    def updateGamePage(self):
        widget = QWidget()
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        background.setStyleSheet(
            "background-image: url(./assets/backgrounds/fond table.PNG)")

        numDealerCards = len(self.game.dealerHand.hand)
        for c in range(numDealerCards):
            cardDrawing = QLabel(widget)
            x = int(WINDOW_WIDTH/2 - (CARD_WIDTH + 25 *
                                      (numDealerCards - 1 - c)) / 2 + 25 * c)
            y = 70
            cardDrawing.setGeometry(x, y, CARD_WIDTH, CARD_HEIGHT)
            cardDrawing.setStyleSheet(
                "border-image: url({})".format(self.game.dealerHand.hand[c].getCardFile()))

        numPlayerCards = len(self.game.playerHand.hand)
        for c in range(numPlayerCards):
            cardDrawing = QLabel(widget)
            x = int(WINDOW_WIDTH/2 - (CARD_WIDTH + 25 *
                                      (numPlayerCards - 1 - c)) / 2 + 25 * c)
            y = 500
            cardDrawing.setGeometry(x, y, CARD_WIDTH, CARD_HEIGHT)
            cardDrawing.setStyleSheet(
                "border-image: url({})".format(self.game.playerHand.hand[c].getCardFile()))

        return widget

    def hitEvent(self):
        self.game.playerTurn()
        if not self.exitGame:
            self.gamePage()

    def standEvent(self):
        while self.game.dealerHand.handValue() <= self.game.playerHand.handValue() or self.game.dealerHand.handValue() <= 17:
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec_()
            self.game.dealerTurn()
            if not self.exitGame:
                self.gamePage()

        self.status = 1

    def win(self):
        self.game.updateScorePlayer()

    def lost(self):
        self.game.updateScoreDealer()

    def leavePage(self):
        # add buttons for game page
        self.exitGame = True
        saveButton = QPushButton("Save Model")
        confirmButton = QPushButton("Confirm Leave")
        saveButton.setStyleSheet(buttonStyle)
        confirmButton.setStyleSheet(buttonStyle)

        widget = QWidget()

        hbox = QHBoxLayout()
        hbox.addWidget(saveButton, alignment=Qt.AlignBottom)
        hbox.addWidget(confirmButton, alignment=Qt.AlignBottom)

        # set the background image for leaving the game
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        background.setStyleSheet(
            "background-image: url(./assets/backgrounds/fond au revoir.PNG)")

        widget.setLayout(hbox)
        self.setCentralWidget(widget)

        saveButton.clicked.connect(self.saveModel)
        confirmButton.clicked.connect(sys.exit)

    def saveModel(self):
        brain.save(self.game.scores['dealer'],
                   self.game.scores['player'])
        sys.exit()

    def loadModel(self):
        brain.load()
        self.game.scores['dealer'] = brain.last_vicDealer
        self.game.scores['player'] = brain.last_vicPlayer
        self.handleGame()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
