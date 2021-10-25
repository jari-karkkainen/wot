# coding: utf-8
"""
A game of fortune and cunning.

The point is to play wheel of fortune with Tractatus logico-philosophicus
verses. The code can be used with any other set of strings. See class
Tractatus.
"""

# In[13]:


# imports
from tractatusplayer import Player
from tractatusfile import Tractatus
from wheeltractatus import Wheel
from tractatusmessages import TractatusMessages
from pyfiglet import figlet_format
from colorama import init
from colorama import Fore, Back, Style
import json
import os
import glob
from time import gmtime, strftime
init()

# In[158]:


class WheelOfTractatus:
    """
    The main game.

    Handles the mainloop, guessing, buing and solving the verses.
    """

    AUTHOR = 'Jari Kärkkäinen'
    AUTHOREMAIL = 'jari.karkkainen@utu.fi'
    VERSION = 0.1
    VERSIONDATE = '10/2021'

    def __init__(self):

        self.mode = 'random'
        self.difficulty = 'hard'
        self.lang = 'fi'
        self.tlang = 'de'
        self.players = []
        self.cplayer = None
        self.cverse = None
        self.solvestring = ''
        self.cspecials = ''
        self.ckey = None
        self.sstring = None
        self.completed = []
        self.filename = None
        self.possibleactions = None
        self.vowelprice = 1000
        self.solvebonus = 500
        self.tm = TractatusMessages()
        self.m = self.tm.m
        '''TractatusMessages object'''
        self.tractatus = Tractatus()
        self.wheel = Wheel()
        # self.start()

    def getInput(self, inputtype='guess'):
        """
        Get the user input from keyboard.

        return codes

        Parameters
        ----------
        inputtype : string, optional
            Parameter inputtype specifies whether user tries to
            'guess' a consonant, 'buy' a vowel, 'solve' the verse or if they
            are giving 'action' commands or setting 'lang' or 'name' in
            settings.
            The default is 'guess'

        Returns
        -------
        userinput : int, char or string
            Input given by user. Type depends on the action user is
            performing.
        exitcode : int
            0: all well
            1: Guessed vowel instead of a consonant
            2: Tried to buy something else than a vowel
            3: User entered a number.
            4: User entered non-alphanumeric character.
            5: Non-numeric action command.
            6: Guessed an already removed consonant.
            -1: Illegal inputtype

        """
        userinput = ''
        exitcode = -1
        if inputtype == 'guess':
            cmdinput = self.m['cmdguess']
        elif inputtype == 'buy':
            cmdinput = self.m['cmdbuy']
        elif inputtype == 'solve':
            cmdinput = self.m['cmdsolve']
        elif inputtype == 'action':
            cmdinput = self.m['cmdaction']
        elif inputtype == 'lang':
            cmdinput = self.m['cmdlang']
        elif inputtype == 'name':
            cmdinput = self.m['cmdname']
        else:
            cmdinput = 'There is an error in getInput()' + inputtype

        while len(userinput) == 0:
            userinput = input(cmdinput + ' ')

        if inputtype != 'solve' and inputtype != 'name':
            userinput = userinput[0]

        if (inputtype == 'action'
                or inputtype == 'lang') and userinput.isnumeric():
            userinput = int(userinput)
            exitcode = 3
        else:
            exitcode = 5

        if inputtype == 'guess':
            if userinput in self.wheel.consonants:
                exitcode = 0
            elif userinput in self.wheel.vowels:
                exitcode = 1
        elif inputtype == 'buy':
            if userinput in self.wheel.vowels:
                exitcode = 0
            else:
                exitcode = 2

        return userinput, exitcode

    def guessConsonant(self):
        """
        Guess a consonant.

        Parameters
        ----------
        verse : TYPE
            DESCRIPTION.

        Returns
        -------
        guessed : char
            DESCRIPTION.
        showstring : string
            DESCRIPTION.
        code : int
            0: all well
            1: User tried to guess already guessed consonant
            2: No instances of consonant in verse
        amount : int
            Amount of instances of consonants in verse.

        """
        code = -1
        hint = 0

        while code != 0:
            guessed, code = self.getInput('guess')
            if(hint > 1):
                print('Type a consonant:', self.wheel.consonants)
            hint = hint + 1

        if guessed.lower() not in self.wheel.removed:
            amount = self.getAmount(guessed)
        else:
            amount = -1

        if amount > 0:
            code = self.wheel.removeChar(guessed)
            self.updateShowstring()
        elif amount == -1:
            code = 1
        else:
            code = 2

        return guessed, code, amount

    def buyVowel(self):
        """
        Buy a vowel.

        Called when user wants to buy a vowel or when they have a chance to
        get a new vowel

        Parameters
        ----------
        verse : string
            Unmasked verse.

        Returns
        -------
        guessed :char
            The vowel the user chose.
        showstring : string
            Verse in mask.
        code : int
            Return codes:
            0: all well
            1: Tried to buy already bought vowel
            2: No instances of vowel in verse
        amount : int
            Number of instances of bought vowels in the verse.

        """
        code = -1
        hint = 0
        while code != 0:
            guessed, code = self.getInput('buy')
            if(hint > 1):
                print('Type a vowel:', self.wheel.vowels)
            hint = hint + 1

        if guessed.lower() not in self.wheel.removed:
            amount = self.getAmount(guessed)
        else:
            amount = -1

        if amount > 0:
            code = self.wheel.removeChar(guessed)
            self.updateShowstring()
        elif amount == -1:
            code = 1
        else:
            code = 2

        return guessed, code, amount

    def solve(self):
        """
        Try to solve current verse.

        Compares user input to solvestring specified in setCurrentverse()

        Returns
        -------
        bool
            True if it is a match, False if not.

        """
        guessed, code = self.getInput('solve')
        # print(self.solvestring)
        # print(guessed)

        if self.solvestring == guessed:
            return True
        else:
            return False

    def getAmount(self, char):
        """
        Get the amount of specified char in current verse.

        Parameters
        ----------
        char : char
            Character to be searched.

        Returns
        -------
        a : int
            Amount of characters.

        """
        a = self.cverse.count(char.lower()) + self.cverse.count(char.upper())
        return a

    def getAction(self, action='action'):
        """
        Get the numeric action key.

        Parameters
        ----------
        action : string
            Either 'action' while in game, or 'lang' while making settings.

        Returns
        -------
        num : int
            Number given by user.
        code : int
            Always 3 as returned by getInput.

        """
        code = -1
        hint = 0

        # print(self.possibleactions.keys())
        while code != 3:
            num, code = self.getInput(action)

            if(hint > 1):
                self.msg(self.m['hintaction'])
                print(self.possibleactions)
            hint = hint + 1

        return num, code

    def getRemainingPoints(self):
        """
        Get the remaining points of verse.

        Used when solving the verse. Gives a flat 100 points per remaining
        character. For example, if verse = 'This is a verse.' and
        showstring = 'T••s •s a •erse' total points is 4 * 100 points.

        Returns
        -------
        points : int
            Amount of points.

        """
        points = 0
        for c in self.sstring:
            if c == '•':
                points = points + 100

        return points

    def setCurrentVerse(self, mode='random'):
        """
        Get a verse from Tractatus object.

        Setting a current verse to be solved.
        TODO: Now only random, later possibility to get next if the player
        wants to play in order from 1 to 7

        Parameters
        ----------
        mode : string, optional
            DESCRIPTION. The default is 'random'.

        Returns
        -------
        None.
        """
        self.solvestring = ''
        self.cspecials = ''
        if self.mode == 'random':
            v, k = self.tractatus.getRandom(not_these=self.completed)
        else:
            v, k = self.tractatus.getNext(not_these=self.completed)
        for c in v:
            if c in self.wheel.playchars or c in self.wheel.punctuation:
                self.solvestring = self.solvestring + c
            else:
                self.solvestring = self.solvestring + '*'
                if c not in self.cspecials:
                    self.cspecials =  self.cspecials + c

        self.cverse = v
        self.ckey = k

    def updateShowstring(self):
        """
        Update the mystery string shown to user.

        Uses character '•' to mask letters in the verse. Leaves special
        characters, like Greek letters, and punctuation intact.

        Returns
        -------
        None.

        """
        showstring = ''
        for char in self.cverse:

            if char not in self.wheel.playchars:
                showstring = showstring + char
            else:
                showstring = showstring + '•'

        self.sstring = showstring

    def addPlayer(self, player):
        """
        Add player to the players list.

        Function checks whether the player is Player. If not then TODO

        Parameters
        ----------
        player : Player
            An instance of Player class.

        Returns
        -------
        None.

        """
        if isinstance(player, Player):
            self.players.append(player)
        else:
            print('addPlayer TODO')

    def showControls(self, action):
        """
        Show appropriate controls.

        Parameters
        ----------
        action : int
            Action code that determines, which set of controls should be
            shown.

        Returns
        -------
        None.

        """
        if action == 99:
            # in the beginning and after guessing a consonant
            print(self.m['controlspin'] + ': 1')
            print(self.m['controlbuy'] + ': 2')
            print(self.m['controlsolve'] + ': 3')
            self.possibleactions = {1: self.m['controlspin'],
                                    2: self.m['controlbuy'],
                                    3: self.m['controlsolve'],
                                    0: self.m['controlexit'],
                                    9: self.m['controlstat']
                                    }
        elif action == 98:
            # after free vowel or bought vowel
            print(self.m['controlspin'] + ': 1')
            print(self.m['controlsolve'] + ': 3')
            self.possibleactions = {1: self.m['controlspin'],
                                    3: self.m['controlsolve'],
                                    0: self.m['controlexit'],
                                    9: self.m['controlstat']
                                    }
        # print('Exit: 0')

    def err(self):
        """
        Show default errormessage if user enters something unknown.

        Returns
        -------
        None.

        """
        print(Fore.YELLOW, Back.RED, self.m['HAL9000'])
        print(Style.RESET_ALL)


    def start(self):
        """
        Create Players and set languages of the game.

        1. Select user interface language.
        2. Ask if we are starting a new game or if a previous game
           should be loaded.

           2.1. If new game. TODO Ask if players should be loaded.

                2.1.1. If new() from the scratch, add players.

                2.1.2. TODO If load players, load them from savefiles.

                2.1.3. Set Tractatus language.

                2.1.4. Set game mode: random or successive.

            2.2. If previous game, load() previous players and game data
            from savefiles. Now there is no need to set mode or Tractatus
            language.

        Returns
        -------
        None.

        """
        print('Valitse kieli, jolla haluat pelata. Suomi = 1, englanti = 2')
        print('Select the game interface language. Finnish =  1, English = 2')

        step = False
        while step is False:
            num, code = self.getAction('lang')
            if num == 1:
                self.lang = 'fi'
                step = True
            elif num == 2:
                self.lang = 'en'
                step = True
            else:
                self.err()

        self.tm.setLanguage(self.lang)
        self.m = self.tm.m

        # Start a new game or load a previous game? New =  1, Load = 2'
        self.msg(self.m['neworload'], 'question')
        self.msg(self.m['new'], 'question')
        self.msg(self.m['load'], 'question')
        step = False
        newgame = True
        while step is False:
            num, code = self.getAction('action')
            if num == 1:
                newgame = True
                step = True
            elif num == 2:
                newgame = False
                step = True
            else:
                self.err()

        if newgame:
            self.new()
        else:
            if self.load() is False:
                self.new()

        self.tractatus = Tractatus(lang=self.tlang)
        self.wheel = Wheel(lang=self.tlang)

    def new(self):
        """
        Star a new game.

        Adding players and setting the Tractatus language.
        Setting game mode next/random and difficulty easy/hard

        Returns
        -------
        None.

        """
        # Adding players
        self.msg(self.m['newstart'], 'info')
        self.msg(self.m['addatleastone'])
        moreplayers = True
        addanother = True
        while moreplayers:
            name, code = self.getInput('name')
            p = Player(name)
            self.addPlayer(p)
            self.msg(self.m['added'].format(p.name), 'info')
            addanother = True
            while addanother:
                self.msg(self.m['addanother'], 'question')
                self.msg(self.m['yes'], 'question')
                self.msg(self.m['no'], 'question')
                num, code = self.getAction('action')
                if num == 2:
                    moreplayers = False
                    addanother =  False
                elif num == 1:
                    addanother = False
                else:
                    self.err()

        # Set the Tractatus language
        self.msg(self.m['settlang'], 'question')
        step = False
        while step is False:
            lang, code = self.getAction('lang')
            if lang == 1:
                self.tlang = 'de'
                step = True
            elif lang == 2:
                self.tlang = 'en'
                step = True
            else:
                self.err()

        # Set game mode
        self.msg(self.m['setmode'], 'question')
        self.msg(self.m['setmodernd'], 'question')
        self.msg(self.m['setmodenext'], 'question')
        step = False
        while step is False:
            mode, code = self.getAction('action')
            if mode == 1:
                self.mode = 'random'
                step = True
            elif mode == 2:
                self.mode = 'next'
                step = True
            else:
                self.err()

        # Set game difficulty
        self.msg(self.m['setdif'], 'question')
        self.msg(self.m['setdifguide'], 'question')
        self.msg(self.m['setdifeasy'], 'question')
        self.msg(self.m['setdifhard'], 'question')
        step = False
        while step is False:
            dif, code = self.getAction('action')
            if dif == 1:
                self.difficulty = 'easy'
                step = True
            elif dif == 2:
                self.difficulty = 'hard'
                step = True
            else:
                self.err()

    def addCompleted(self):
        """
        Add the current verse into solved verses.

        The point is to not guess the same verse twice in the same game.

        Returns
        -------
        None.

        """
        self.completed.append({self.ckey: self.tlang})

    def showStats(self):
        """
        Show the game statistics.

        Shows te game statistics, player info, wheel sectors and some guidance.

        Returns
        -------
        None.

        """
        print(Fore.LIGHTYELLOW_EX)
        print(' Completed verses: {0}'.format(self.completed))
        print(' Current player: {0}'.format(self.cplayer.name))
        print(' Current verse: {0}'.format(self.ckey))
        print(' Userinterface language: {0}'.format(self.lang))
        print(' Tranctatus language: {0}\n'.format(self.tlang))
        print(' Player stats:')

        for p in self.players:
            print(' ', p.getData())

        print()
        print(' Sectors of the wheel {0}\n'.format(self.wheel.sectors))
        print(' To end the game, give action: 0.')
        print(Fore.RESET)

    def msg(self, msg, style='default'):
        """
        Print text in colour.

        Parameters
        ----------
        msg : string
            Message to print.
        style : string, optional
            Possible values are: warn, congrat, info and question.
            The default is 'default'.

        Returns
        -------
        None.

        """
        color = Fore.RESET
        if style == 'warn':
            color = Fore.RED
        elif style == 'congrat':
            color = Fore.CYAN
        elif style == 'info':
            color = Fore.LIGHTYELLOW_EX
        elif style == 'question':
            color = Fore.LIGHTBLUE_EX

        print(color + msg + Fore.RESET)

    def play(self):
        """
        Play the game.

        Game main loop. Goes on until action 0 is given.

        Returns
        -------
        None.

        """
        self.cls()
        self.credits()
        # print('Starting the Language game!')

        action = 100
        cycle = -1

        while action != 0:
            cycle = cycle + 1

            # print('Action is', action)
            # print('Cycle is', cycle)
            #print()

            if(cycle > 0):
                cp = cycle % len(self.players)
                self.cplayer = self.players[cp]
                if action > 90 and action < 100:
                    print(' {0} : {1} points. \n'.format(self.cplayer.name,
                                                     self.cplayer.points))
                    if self.difficulty == 'easy':
                        print(self.m['pckey'], ' ' ,self.ckey)
                    print(self.sstring)
                    self.showControls(action)

            if action == 100:
                # starting with a new sentence
                self.msg(self.m['pnew'], 'info')
                self.wheel.setPlayChars()
                self.setCurrentVerse()
                self.wheel.setRemoved(self.difficulty)
                msg = self.m['revealed']
                for char in self.wheel.removed:
                    msg = msg + char + ' '
                self.msg(msg, 'info')

                self.updateShowstring()
                action = 99
            elif action == 99 or action == 98:
                action, code = self.getAction()
                cycle = cycle - 1
            elif action == 1:
                self.wheel.spin()
                if self.wheel.activesector == 'thief':
                    action = 13
                elif self.wheel.activesector == 'free':
                    action = 12
                else:
                    action = 11
                cycle = cycle - 1
            elif action == 2:
                # Buing a vowel.
                if self.cplayer.points >= self.vowelprice:
                    self.msg(self.m['pbuyvowel'], 'question')
                    g, code, amount = self.buyVowel()
                    self.cplayer.subtract(self.vowelprice)
                    if code == 1:
                        # Tried to buy alredy revealed vowel
                        self.cplayer.addVowel(-1)
                        self.msg(self.m['pbuyalready'], 'warn')
                        self.msg(self.m['pchangeturn'], 'info')
                        action = 99
                    else:
                        self.cplayer.addVowel(1)
                        print(self.m['pselected'].format(g, amount))
                        print(self.m['pcontinue'])
                        cycle = cycle - 1
                        action = 98
                else:
                    self.msg(self.m['pnomoney'], 'warn')
                    print(self.m['pcontinue'])
                    cycle = cycle - 1
                    action = 98
            elif action == 3:
                # Solving the sentence
                print(self.m['psolvetry'].format(self.cplayer.name))
                if len(self.cspecials) > 0:
                    # if there are special characters in the sentence,
                    # show information how to handle them.
                    self.msg(self.m['psolveguide'].format(self.cspecials),
                             'info')

                if self.solve():
                    points = self.solvebonus + self.getRemainingPoints()
                    self.cplayer.addPoints(points)
                    self.cplayer.addCompleted(self.ckey, self.tlang)
                    self.completed.append(self.ckey)
                    self.msg(self.m['psolvec1'], 'congrat')
                    self.msg(self.m['pgetpoints'].format(points), 'congrat')
                    self.msg(self.m['psolvec3'].format(self.cplayer.name, self.ckey), 'congrat')
                    self.msg(self.cverse, 'congrat')

                    print(self.m['pcontinue'])

                    cycle = cycle + 1
                    action = 100
                else:
                    self.msg(self.m['psolvefail'], 'warn')
                    if len(self.players) > 1:
                        self.msg(self.m['pchangeturn'], 'info')
                    action = 99
            elif action == 11:
                # Wheel was spinned and landed on consonant guessing sector.
                self.msg(self.m['pgguide'].
                         format(self.cplayer.name), 'info')
                self.msg(self.m['pgsector'].
                         format(self.wheel.activesector), 'info')
                g, code, amount = self.guessConsonant()
                if code == 1:
                    self.msg(self.m['pgalready'], 'warn')
                else:
                    print(self.m['pselected'].format(g, amount))
                if amount > 0:
                    self.cplayer.addConsonant(1)
                    points = amount * self.wheel.activesector
                    self.msg(self.m['pgetpoints'].format(points), 'congrat')
                    self.cplayer.addPoints(points)
                    print(self.m['pcontinue'])
                    cycle = cycle - 1
                else:
                    self.msg(self.m['pgfail'], 'warn')
                    self.cplayer.addConsonant(-1)
                    if len(self.players) > 1:
                        self.msg(self.m['pchangeturn'], 'info')
                action = 99
            elif action == 12:
                # Wheel was spun and landed on free sector!
                self.msg(self.m['pfsector'], 'congrat')
                self.msg(self.m['pffree'].format(self.cplayer.name), 'congrat')
                g, code, amount = self.buyVowel()
                if code == 1:
                    # Tried to select alredy revealed vowel
                    self.msg(self.m['pfreealready'], 'info')
                else:
                    self.cplayer.addFree()
                    print(self.m['pselected'].format(g, amount))
                cycle = cycle - 1
                action = 98
            elif action == 13:
                # Wheel was spun and landed on thief sector!
                self.msg(self.m['prob'], 'warn')
                self.msg(self.m['probbed'].format(self.cplayer.name), 'warn')
                self.msg(self.m['problose'], 'warn')
                if len(self.players) > 1:
                    self.msg(self.m['pchangeturn'], 'info')
                self.cplayer.setLost()
                action = 99
            elif action == 0:
                self.end()
            elif action == 9:
                self.showStats()
                cycle = cycle - 1
                action = 99
            else:
                self.err()
                action = 99
                cycle = cycle - 1

        self.end()

    def end(self):
        """
        End the game.

        1. Ask if user wants to save progress
        1.1. If yes, save game progress
        1.2. If yes, save players
        2. Exit

        Returns
        -------
        None.

        """
        # Do you want to save progress before closing the game?'
        self.msg(self.m['endsave'], 'question')
        self.msg(self.m['yes'], 'question')
        self.msg(self.m['no'], 'question')
        step = False
        while step is False:
            num, code = self.getAction('action')
            if num == 1:
                if self.filename == None:
                    # Give savegame an identifier
                    self.msg(self.m['endidentifier'], 'info')
                    filepostfix, code = self.getInput('name')
                    self.filename = self.save(filepostfix)
                else:
                    self.filename = self.save(None)
                self.msg(self.m['endsavedas'].format(self.filename), 'info')
                #for player in self.players:
                #    filename = player.save(self.filename)
                #    msg = self.m['endsavedplayeras'].format(player.name,
                #                                            filename)
                #    self.msg(msg, 'info')
                step = True
            elif num == 2:
                step = True
            else:
                self.err()
        # Exit
        self.credits(ending = True)

    def save(self, filename):
        """
        Save the game.

        Saves the game progress and players in formatted json as
        WoT_filename.json

        Parameters
        ----------
        filename : string
            Filename identifier.

        Returns
        -------
        filename : string
            Full filename.

        """
        if filename is None:
            filename = self.filename
        else:
            filename = 'WoT_' + filename + '.json'
        data = {'filename': filename,
                'playtime': strftime("%Y-%m-%d %H:%M", gmtime()),
                'version': self.VERSION,
                'mode': self.mode,
                'difficulty': self.difficulty,
                'lang': self.lang,
                'tlang': self.tlang,
                'completed': self.completed,
                'cverse': self.cverse,
                'ckey': self.ckey,
                'solvestring': self.solvestring,
                'sstring': self.sstring,
                'cplayer': self.cplayer.name,
                'players': []
                }
        for player in self.players:
            data['players'].append(player.getData())

        file = 'save/' + filename

        with open(file, 'w') as savefile:
            savefile.write(json.dumps(data, indent=4))

        return filename

    def load(self):
        """
        Load a saved game.

        1. Check if there are saved games.
        1.1. If there are
        1.2. If there are no saved games, return False.

        Returns
        -------
        ret bool
            DESCRIPTION.

        """
        ret = False

        self.msg(self.m['loadstart'], 'info')

        savefiles = []
        for file in glob.glob("save\*.json"):
            savefiles.append(file)

        if len(savefiles) > 0:

            filenames = []
            for j in savefiles:
                with open(j, 'r') as save:
                    content = json.loads(save.read())
                    filenames.append(content['filename'] +
                                     ' ' + content['playtime'])

            # msg = ' Which save you want to load?\n'
            self.msg(self.m['loadwhich'], 'question')

            counter = 0
            for fn in filenames:
                counter = counter + 1
                self.msg('{0} = {1}'.format(counter, fn), 'question')

            userinput = 0
            self.possibleactions = range(1, counter)
            while userinput < 1 or userinput > counter:
                userinput, code = self.getAction('action')

            self.msg(self.m['loadthis'].format(filenames[userinput-1]), 'info')

            with open(savefiles[userinput-1], 'r') as save:
                content = json.loads(save.read())

                self.filename = content['filename']
                self.mode = content['mode']
                self.difficulty = content['difficulty']
                #self.lang =
                self.tlang = content['tlang']
                self.completed = content['completed']
                for p in content['players']:
                    player = Player(loaduser = p)
                    self.players.append(player)
            ret = True

        else:
            self.msg(self.m['loadnofiles'], 'warn')
            ret = False

        return ret

    def cls(self):
        """
        Clear the console.

        Returns
        -------
        None.

        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def credits(self, ending=False):
        """
        Display gema credits.

        Parameters
        ----------
        ending : bool, optional
            If True, show also a message of the day. The default is False.

        Returns
        -------
        None.

        """
        print(Fore.GREEN)
        print(figlet_format('Wheel of Tractatus'))
        print(self.m['credittitle'])
        print(self.m['creditauthor'].format(WheelOfTractatus.AUTHOR,
                                            WheelOfTractatus.AUTHOREMAIL))
        print(self.m['creditversion'].format(WheelOfTractatus.VERSION,
                                             WheelOfTractatus.VERSIONDATE))
        if ending:
            print()
            print(self.m['creditmsgoftheday'])
            print(self.tractatus.getRandom()[0])
        print(Fore.RESET)


'''
Starting the game
'''
# WheelOfTractatus.credits(None)

game = WheelOfTractatus()
game.credits()
game.start()
game.play()
