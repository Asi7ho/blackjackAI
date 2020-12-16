import sys

from game import Game
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time

WINDOW_WIDTH = 1136
WINDOW_HEIGHT = 850
CARD_WIDTH = 167
CARD_HEIGHT = 225

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

        # window
        self.setWindowTitle("Black Jack ++")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # launch
        self.homePage()
        self.show()
        self.status = 0

    def homePage(self):
        # add buttons for home page
        rulesButton = QPushButton("Rules")
        rulesButton.setStyleSheet(buttonStyle)
        rulesButton.clicked.connect(self.rulesPage)

        scoreButton = QPushButton("Scores")
        scoreButton.setStyleSheet(buttonStyle)
        scoreButton.clicked.connect(self.scoresPage)

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox.addWidget(rulesButton)
        hbox.addWidget(scoreButton)

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
        playButton.clicked.connect(self.processGame)

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

    def scoresPage(self):
        # add buttons for scores page
        backButton = QPushButton("Back")
        backButton.setStyleSheet(buttonStyle)
        backButton.clicked.connect(self.homePage)

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)

        # add widgets
        wrapperScoreV = QVBoxLayout()
        wrapperScoreV.setContentsMargins(20, 120, 0, 0)
        _, keys, values = self.game.getScores()
        numScoresToPlot = min(15, len(keys))
        for rank in range(numScoresToPlot):
            wrapperScoreH = QHBoxLayout()
            labelName = QLabel("{}".format(keys[rank]))
            labelName.setFont(QFont('Arial', 26))
            labelScore = QLabel("{}".format(values[rank]))
            labelScore.setFont(QFont('Arial', 26))
            wrapperScoreH.addWidget(labelName)
            wrapperScoreH.addWidget(labelScore)
            wrapperScoreH.addStretch(1)
            wrapperScoreV.addLayout(wrapperScoreH)

        vbox.addLayout(wrapperScoreV)
        vbox.addStretch()
        vbox.addLayout(hbox)
        hbox.addWidget(backButton)

        widget = QWidget()

        # set the background image as the scores page
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        background.setStyleSheet(
            "background-image: url(./assets/backgrounds/fond score.PNG)")

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def gamePage(self):
        # add buttons for game page
        hitButton = QPushButton("Hit")
        hitButton.setStyleSheet(buttonStyle)
        hitButton.clicked.connect(self.hitEvent)

        standButton = QPushButton("Stand")
        standButton.setStyleSheet(buttonStyle)
        standButton.clicked.connect(self.standEvent)

        splitButton = QPushButton("Split")
        splitButton.setStyleSheet(buttonStyle)
        splitButton.clicked.connect(self.splitEvent)

        leaveButton = QPushButton("Leave")
        leaveButton.setStyleSheet(buttonStyle)
        leaveButton.clicked.connect(self.leavePage)

        # add players name
        labelDealer = QLabel("Dealer: {}".format(
            self.game.dealerHand.handValue()))
        labelDealer.setFont(QFont('Arial', 26))
        labelDealer.setStyleSheet(
            "padding:5px 20px; color: white; background-color:rgb(43, 43, 43); border-radius:20px")
        labelPlayer = QLabel("You: {}".format(
            self.game.playerHand.handValue()))
        labelPlayer.setFont(QFont('Arial', 26))
        labelPlayer.setStyleSheet(
            "padding:5px 20px; color: white; background-color:rgb(43, 43, 43); border-radius:20px")

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)

        # add widgets
        wrapperGameV = QVBoxLayout()

        # label Dealer
        wrapperGameV.addWidget(labelDealer, alignment=Qt.AlignCenter)

        # label player
        wrapperGameV.addStretch()
        wrapperGameV.addWidget(labelPlayer, alignment=Qt.AlignCenter)

        vbox.addLayout(wrapperGameV)
        vbox.addLayout(hbox)

        hbox.addWidget(hitButton)
        hbox.addWidget(standButton)
        # hbox.addWidget(splitButton)
        hbox.addWidget(leaveButton)

        vbox.addLayout(wrapperGameV)

        widget = self.updateGamePage()

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        if self.game.dealerHand.handValue() == 21 and len(self.game.dealerHand.hand) == 2:
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            self.lostPage()
            return

        if self.game.playerHand.handValue() == 21 and len(self.game.playerHand.hand) == 2:
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            self.winPage()
            return

        if self.game.playerHand.handValue() > 21:
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            self.lostPage()
            return

        if self.game.dealerHand.handValue() > 21:
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            self.winPage()
            return

        if self.status == 1:
            if self.game.dealerHand.handValue() >= self.game.playerHand.handValue():
                loop = QEventLoop()
                QTimer.singleShot(1000, loop.quit)
                loop.exec_()
                self.lostPage()

    def processGame(self):
        self.gamePage()

        # game
        loop = QEventLoop()
        QTimer.singleShot(500, loop.quit)
        loop.exec_()
        self.game.dealerTurn()
        self.gamePage()

        loop = QEventLoop()
        QTimer.singleShot(500, loop.quit)
        loop.exec_()
        self.game.playerTurn()
        self.gamePage()

        loop = QEventLoop()
        QTimer.singleShot(500, loop.quit)
        loop.exec_()
        self.game.playerTurn()
        self.gamePage()

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
        self.gamePage()

    def standEvent(self):
        while self.game.dealerHand.handValue() <= self.game.playerHand.handValue():
            loop = QEventLoop()
            QTimer.singleShot(500, loop.quit)
            loop.exec_()
            self.game.dealerTurn()
            self.gamePage()

        self.status = 1
        self.gamePage()

    def splitEvent(self):
        pass

    def winPage(self):
        # add buttons for win page
        continueButton = QPushButton("Continue")
        continueButton.setStyleSheet(buttonStyle)
        continueButton.clicked.connect(self.newGame)

        leaveButton = QPushButton("Leave")
        leaveButton.setStyleSheet(buttonStyle)
        leaveButton.clicked.connect(self.leavePage)

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox.addWidget(continueButton)
        hbox.addWidget(leaveButton)

        widget = QWidget()

        # set the background image for leaving the game
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        background.setStyleSheet(
            "background-image: url(./assets/backgrounds/fond gagne.PNG)")

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.game.updateScorePlayer()

    def lostPage(self):
        # add buttons for win page
        continueButton = QPushButton("Continue")
        continueButton.setStyleSheet(buttonStyle)
        continueButton.clicked.connect(self.newGame)

        leaveButton = QPushButton("Leave")
        leaveButton.setStyleSheet(buttonStyle)
        leaveButton.clicked.connect(self.leavePage)

        # layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox.addWidget(continueButton)
        hbox.addWidget(leaveButton)

        widget = QWidget()

        # set the background image for leaving the game
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        if self.game.dealerHand.handValue() == 21 and len(self.game.dealerHand.hand) == 2:
            background.setStyleSheet(
                "background-image: url(./assets/backgrounds/fond perdu blackjack.PNG)")
        else:
            background.setStyleSheet(
                "background-image: url(./assets/backgrounds/fond perdu.PNG)")

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.game.updateScoreDealer()

    def newGame(self):
        self.game.resetHands()
        self.status = 0
        self.processGame()

    def leavePage(self):
        # add buttons for game page
        confirmButton = QPushButton("Confirm")
        confirmButton.setStyleSheet(buttonStyle)

        # add widgets
        label = QLabel("Enter your name:")
        label.setFont(QFont('Arial', 26))

        self.lineEdit.setStyleSheet(
            "padding:5px 10px")

        # layout
        wrapperLE = QVBoxLayout()
        wrapperLE.setContentsMargins(500, 50, 250, 650)
        wrapperLE.addStretch()
        wrapperLE.addWidget(label, alignment=Qt.AlignTop)
        wrapperLE.addWidget(self.lineEdit, alignment=Qt.AlignTop)
        wrapperLE.addWidget(confirmButton, alignment=Qt.AlignTop)

        widget = QWidget()

        # set the background image for leaving the game
        background = QLabel(widget)
        background.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        background.setStyleSheet(
            "background-image: url(./assets/backgrounds/fond au revoir.PNG)")

        widget.setLayout(wrapperLE)
        self.setCentralWidget(widget)

        confirmButton.clicked.connect(self.registerUser)

    def registerUser(self):
        if self.lineEdit.text() != "":
            self.username = self.lineEdit.text()

        self.game.scores[self.username] = self.game.scores['player']
        self.game.saveGameScore()
        sys.exit()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
