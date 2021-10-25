# -*- coding: utf-8 -*-
"""
Part of the game Wheel of Tractatus.

Author Jari Kärkkäinen
Author email: jari.karkkainen@utu.fi
"""

# In[13]:

import random


# In[158]:

class Wheel:
    """
    The wheel of the game.

    Handles control of sectors and character lists.
    """

    def __init__(self, lang='fi'):
        self.consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                           'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'å', 'ä', 'ö']
        self.punctuation = ['.', ',', ':', ';',
                            '?', '!', ' ', '"', "'",
                            '-', '=', '&', '%', '#', '+', '*',
                            '(', ')', '{', '}',
                            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.playchars = None

        self.setLanguage(lang)

        # self.setAllChars()
        # self.sectors = {1: 50, 2: 100, 3: 'thief', 4: 'free'}
        self.sectors = {1: 50,
                        2: 50,
                        3: 50,
                        4: 50,
                        5: 75,
                        6: 75,
                        7: 75,
                        8: 75,
                        9: 100,
                        10: 100,
                        11: 100,
                        12: 100,
                        13: 125,
                        14: 125,
                        15: 125,
                        16: 125,
                        17: 150,
                        18: 150,
                        19: 150,
                        20: 150,
                        21: 250,
                        22: 500,
                        23: 'thief',
                        24: 'free'}
        self.activesector = None

    def setPlayChars(self):
        """
        Generate current playchars list.

        Returns
        -------
        None.

        """
        self.playchars = [' ']
        self.playchars.extend(self.consonants)
        self.playchars.extend(self.vowels)

        for l in self.consonants:
            self.playchars.append(l.upper())
        for l in self.vowels:
            self.playchars.append(l.upper())

        self.playchars.remove(' ')

    def setRemoved(self, difficulty='hard'):
        """
        Generate a list of removed characters.

        Removes these characters from current playchars.

        Parameters
        ----------
        difficulty : string, optional
            May be 'easy' or 'hard'. The default is 'hard'.

        Returns
        -------
        None.

        """
        self.removed = [' ']
        if difficulty == 'easy':
            rndc = random.sample(self.consonants, 3)
            rndv = random.sample(self.vowels, 1)
            rndc.extend(rndv)
        else:
            rndc = random.sample(self.consonants, 2)

        for char in rndc:
            self.removeChar(char)
        self.removed.remove(' ')

    def setLanguage(self, lang):
        """
        Set the Wheel language.

        Adds or removes vowels å, ä, and ö depending on the lang

        Parameters
        ----------
        lang : string
            Language code 'en', 'de'.

        Returns
        -------
        None.

        """
        self.lang = lang
        if lang == 'en':
            if 'å' in self.vowels:
                self.vowels.remove('å')
            if 'ä' in self.vowels:
                self.vowels.remove('ä')
            if 'ö' in self.vowels:
                self.vowels.remove('ö')
        elif lang == 'de':
            if 'å' in self.vowels:
                self.vowels.remove('å')
            if 'ä' not in self.vowels:
                self.vowels.append('ä')
            if 'ö' not in self.vowels:
                self.vowels.append('ö')

    def removeChar(self, char):
        """
        Remove letter from current playchars.

        Parameters
        ----------
        char : char
            Letter to be removed.

        Returns
        -------
        code : int
            0 if there was letter to remove.
            1 if the letter was not in playchars

        """
        if char.lower() in self.playchars:
            self.playchars.remove(char)
            self.playchars.remove(char.upper())
            self.removed.append(char.lower())
            code = 0
        else:
            code = 1

        return code

    def showSectors(self):
        """
        TODO.

        Returns
        -------
        None.

        """
        print(self.sectors)

    def spin(self):
        """
        Spin the wheel.

        Selects a random sector from sectors and sets it as
        the activesector.

        Returns
        -------
        None.

        """
        r = random.randint(1, len(self.sectors))
        self.activesector = self.sectors[r]
