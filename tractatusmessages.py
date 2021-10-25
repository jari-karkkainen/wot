# -*- coding: utf-8 -*-
"""
Part of the game Wheel of Tractatus.

Author Jari Kärkkäinen
Author email: jari.karkkainen@utu.fi
"""
import pandas as pd

class TractatusMessages():
    """Internationalization object for the game Wheel of Tractatus."""

    def __init__(self, lang = 'fi'):

        self.m = {}
        self.setLanguage(lang)

    def setLanguage(self, lang):
        """
        Set language and read appropriate messages from file.

        The file must have column 'msg' as the key, and a column
        named as lang parameter.


        Parameters
        ----------
        lang : sring
            language code 'en', 'fi'.

        Returns
        -------
        None.

        """
        self.lang = lang
        file = 'data/TractatusMessages.xlsx'
        data = pd.read_excel(file)
        self.m = data[["msg", self.lang]]
        self.m.set_index('msg', inplace=True)
        self.m = self.m.to_dict()[self.lang]
        # print(self.m)
