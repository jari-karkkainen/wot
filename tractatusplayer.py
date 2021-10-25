# -*- coding: utf-8 -*-
"""
Part of the game Wheel of Tractatus.

Author Jari Kärkkäinen
Author email: jari.karkkainen@utu.fi
"""


class Player:
    """Object representing a player in the Wheel of Tractatus."""

    AUTHOR = 'Jari Kärkkäinen'
    AUTHOREMAIL = 'jari.karkkainen@utu.fi'
    VERSION = 0.1
    VERSIONDATE = '10/2021'

    name = 'Language games player'

    def __init__(self, name='Language games player', loaduser=False):
        if loaduser is False:
            self.name = name
            self.points = 0
            self.bought = 0
            self.lost = 0
            self.won = 0
            self.completed = []

            self.consonants = 0
            self.consonantswrong = 0
            self.vowels = 0
            self.vowelswrong = 0
            self.vowelsfree = 0
            self.robbed = 0
        else:
            self.loadData(loaduser)

    def addPoints(self, amount):
        """
        Add points.

        Adds points to Player.points and Player.won.

        Parameters
        ----------
        amount : int
            Amount of points to add..

        Returns
        -------
        None.

        """
        self.points = self.points + amount
        self.won = self.won + self.points

    def addConsonant(self, code):
        """
        Increment counter for either consonants or consonantswrong.

        Parameters
        ----------
        code : int
            If code is 1, increment consonant count, otherwise
            increment wrong consonant count.

        Returns
        -------
        None.

        """
        if code == 1:
            self.consonants = self.consonants + 1
        else:
            self.consonantswrong = self.consonantswrong + 1

    def addVowel(self, code):
        """
        Increment counter for either vowels or vowelswrong.

        Parameters
        ----------
        code : int
            If code is 1, increment vowel count, otherwise
            increment wrong vowel count.

        Returns
        -------
        None.

        """
        if code == 1:
           self.vowels = self.vowels + 1
        else:
           self.vowelswrong = self.vowelswrong + 1

    def addFree(self):
        """
        Add one to free vowels count.

        Returns
        -------
        None.

        """
        self.vowesfree = self.vowelsfree + 1

    def subtract(self, points):
        """
        Subtract points and add points to bought.

        Parameters
        ----------
        points : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.points = self.points - points
        self.bought = self.bought + points

    def setLost(self):
        """
        Set points to 0 and add one to robbed counter.

        Returns
        -------
        None.

        """
        self.lost = self.lost + self.points
        self.points = 0
        self.robbed = self.robbed + 1

    def addCompleted(self, versekey, lang):
        self.completed.append({versekey: lang})

    def getData(self):
        """
        Generate player data for display and saving.

        Returns
        -------
        data : dict
            Collection of player data.

        """
        data = {'name': self.name,
                'version': self.VERSION,
                'points': self.points,
                'bought': self.bought,
                'won': self.won,
                'lost': self.lost,
                'robbed': self.robbed,
                'consonants': self.consonants,
                'consonantswrong': self.consonantswrong,
                'vowels': self.vowels,
                'vowelswrong': self.vowelswrong,
                'vowelsfree': self.vowelsfree,
                'completed': self.completed}
        return data

    def loadData(self, data):
        """
        Load player data.

        Parameters
        ----------
        data : dict

        Returns
        -------
        None.

        """
        self.name = data['name']
        self.points = data['points']
        self.bought = data['bought']
        self.lost = data['lost']
        self.won = data['won']
        self.completed = data['completed']

        self.consonants = data['consonants']
        self.consonantswrong = data['consonantswrong']
        self.vowelswrong = data['vowelswrong']
        self.vowels = data['vowels']
        self.vowelsfree = data['vowelsfree']
        self.robbed = data['robbed']

    def save(self, f):
        """
        Save player data to file.

        TODO Might be useful in future for importing player data.

        Parameters
        ----------
        f : string
            File name or identifier.

        Returns
        -------
        f : TYPE
            DESCRIPTION.

        """
        # print('TODO')
        # data = self.getData()
        return f
