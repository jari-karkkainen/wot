# -*- coding: utf-8 -*-
"""
Part of the game Wheel of Tractatus.

Author Jari Kärkkäinen
Author email: jari.karkkainen@utu.fi
"""
import pandas as pd

class Tractatus:
    """
    Object representing Tractatus logico-philosophicus.

    Description of the object.
    """

    testVerse1 = 'Totuusfunktion yleinen muoto on [ p ¯ , ξ ¯ , N ( ξ ¯ ) ]. Tämä on lauseen yleinen muoto.'
    testVerse = 'Testi'

    def __init__(self, file=None, lang='en'):
        """
        Initialize tractatus.

        Read file contents into dataframe. The data should have columns
        [key, content, lang]

        Parameters
        ----------
        file : string, optional
            Path to optional tractatus file. The default is None and means
            data to be read from data/tractatus.xlsx
        lang : string, optional
            Language code. The default is 'en'.

        Returns
        -------
        None.

        """
        self.data = None

        if file is None:
            file = 'data/tractatus.xlsx'

        self.df = pd.read_excel(file)
        self.setLanguage(lang)


    def setLanguage(self, lang):
        """
        Set the tractatus language.

        Selects only those verses from the total data that are in
        specified language.

        Parameters
        ----------
        lang : string
            Language code 'en', 'de'.

        Returns
        -------
        None.

        """
        self.data = self.df.query('lang == @lang').sort_values('key')
        # self.data = self.data
        self.data.reset_index(inplace=True)

    def getRandom(self, not_these=[]):
        """
        Select random verse from tractatus.

        Parameters
        ----------
        not_these : list
            A list of verse keys that are already solved by the player.
            For example ['3.4.2', 7, '1.0.0.1']. The default is empty list.

        Returns
        -------
        content : string
            The text of the verse e.g. 'Was das Bild darstellt, ist sein Sinn'.
        key : string
            Number key of the verse e.g. '2.2.2.1'.

        """
        if len(not_these) == 0:
            randomVerse = self.data.sample(n=1)
        else:
            key = 0
            content = ''
            # print(len(self.data), '  notthese = ', len(notThese))
            while key in not_these or key == 0:
                randomVerse = self.data.sample(n=1)
                key = randomVerse.iloc[0][1]

        content = randomVerse.iloc[0][2]
        key = randomVerse.iloc[0][1]

        # return Tractatus.testVerse, 0

        return content, key

    def getNext(self, not_these=[]):
        """
        Get the next sentence.

        TODO what if all sentences are solved already?

        Parameters
        ----------
        not_these : list, optional
            List of excluded sentences keys. For example
            ['3.4.2', 7, '1.0.0.1'] The default is empty list.

        Returns
        -------
        content : string
            The text of the verse e.g. 'Jedes Bild ist auch ein logisches.
            (Dagegen ist z. B. nicht jedes Bild ein räumliches.'.
        key : string
            Number key of the verse e.g. '2.1.8.2'.

        """
        if len(not_these) > 0:
            not_these.sort()
            lastkey = not_these[-1]
            lastindex = self.data.index[self.data['key'] == lastkey].tolist()[-1]
            # print(lastindex)
            key = self.data['key'].iloc[lastindex + 1]
            content = self.data['content'].iloc[lastindex + 1]
        else:
            key = self.data['key'].iloc[0]
            content = self.data['content'].iloc[0]


        return content, key

    def get(self, key):
        """
        Get the specific sentence.

        Parameters
        ----------
        key : string
            Tractatus sentence key, e.g. '7' or '6.5.4.1'.

        Returns
        -------
        content : string
            Sentence.
        key : string
            Sentence key.

        """
        keyindex = self.data.index[self.data['key'] == key].tolist()[-1]
        content = self.data['content'].iloc[keyindex]

        return content, key



# tr = Tractatus(lang='en')
# print(tr.get('5.4.6'))
# print(tr.getNext(['5.4.6']))

'''
not_these = ['6.0.1']
for i in range(1,10):
    v, k = tr.getNext(not_these = not_these)
    not_these.append(k)
    print(k)
    print(v)

# for i in range(1, 2000):
    #print()
    #print(tr.getRandom())
'''
