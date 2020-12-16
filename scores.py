"""
    This file handle the save/recover the scores state. 
"""

import os
import pickle
from collections import OrderedDict

from constants import localScoresFile


def getScoresFromFile():
    """
      Recover scores from the scores file defined in constants.py
      The function returns a dictionnary if there if the file exists otherwise it returns an empty dictionary
    """

    if os.path.exists(localScoresFile):
        scoresFile = open(localScoresFile, "rb")
        scoresUnpickle = pickle.Unpickler(scoresFile)
        scores = scoresUnpickle.load()
        scoresFile.close()
    else:
        scores = {}
    return scores


def saveScores(scores):
    """
      Save the scores dictionnary in a local file
    """

    # The previous data are erased
    scoresFile = open(localScoresFile, "wb")
    scoresPickle = pickle.Pickler(scoresFile)
    scoresPickle.dump(scores)
    scoresFile.close()


def sortScores(scores):
    sortedDict = OrderedDict(
        sorted(scores.items(), key=lambda t: t[1], reverse=True))

    keys = []
    values = []
    for v in sortedDict.values():
        values.append(v)

    for k in sortedDict.keys():
        keys.append(k)

    return sortedDict, keys, values
