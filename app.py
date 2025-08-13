"""
Primary module for Alien Invaders

This module contains the main controller class for the Planetoids application.
There is no need for any need for additional classes in this module. If you
need more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Ed Discussions.

Emily Wei (ejw235) and Amira Razack (arr258)
12/11/24

"""
from consts import *
from game2d import *
from wave import *
import json

# PRIMARY RULE: Planetoids can only access attributes in wave.py via getters/setters
# Planetoids is NOT allowed to access anything in models.py

class Planetoids(GameApp):
    """
    The primary controller class for the Planetoids application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class. Any initialization should be done in
    the start method instead. This is only for this class. All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is managing the game state: when is the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state. For a complete description of how the states work, see the
    specification for the method update().

    As a subclass of GameApp, this class has the following (non-hidden) inherited
    INSTANCE ATTRIBUTES:

    Attribute view: the game view, used in drawing (see examples from class)
    Invariant: view is an instance of GView

    Attribute input: the user input, used to control the ship and change state
    Invariant: input is an instance of GInput

    These attributes are inherited. You do not need to add them. Any other attributes
    that you add should be hidden.

    Other Class Attributes:
    Attribute waves: contains a list of the names of the different wave files
    Invariant: waves is a list of strings containing the three different waves

    Attribute wins: serves as a counter if the player won the wave
    Invariant: wins is an int that is incremented when the player wins a wave
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    waves = ['wave1.json','wave2.json','wave3.json']
    wins = 0
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _state: the current state of the game as a value from consts.py
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED,
    #            STATE_ACTIVE, STATE_CONTINUE
    #
    # Attribute _wave: the subcontroller for a single wave, which manages the game
    # Invariant: _wave is a Wave object, or None if there is no wave currently active.
    #            _wave is only None if _state is STATE_INACTIVE.
    #
    # Attribute _title: the game title
    # Invariant: _title is a GLabel, or None if there is no title to display. It is None
    #            whenever the _state is not STATE_INACTIVE.
    #
    # Attribute _message: the currently active message
    # Invariant: _message is a GLabel, or None if there is no message to display. It is
    #            only None if _state is STATE_ACTIVE.
    #
    # Attribute _background: game background (made in Photoshop)
    # Invariant: _background is a GImage, or None if there is no background to
    #           display
    #
    # Attribute _winlosetext: the text that displays "YOU WIN" or "YOU LOSE" at
    #           the end of a wave
    # Invariant: _winlosetext is a GLabel, or None if there is no message to
    #            display

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and creates both
        the title (in attribute _title) and a message (in attribute _message) saying
        that the user should press a key to play a game.
        """
        self._state=STATE_INACTIVE
        self._background = GImage(x=400,y=350,width=GAME_WIDTH,
            height=GAME_HEIGHT,source='space.png')
        self._wave=None
        if self._state==STATE_INACTIVE:
            self._title=GLabel(text="Planetoids", font_size=TITLE_SIZE,
                x=GAME_WIDTH/2, y=(GAME_HEIGHT/2)+TITLE_OFFSET,
                font_name=TITLE_FONT, linecolor='white')
            self._message=GLabel(text="Press s to start",
                font_size=MESSAGE_SIZE, x=GAME_WIDTH/2,
                y=(GAME_HEIGHT/2)+MESSAGE_OFFSET,
                font_name=MESSAGE_FONT,linecolor='white')
        elif self._state==STATE_ACTIVE:
            self._message=None
        else:
            self._title=None
        self._winlosetext = GLabel(text="",
            font_size=120, x=GAME_WIDTH/2,
            y=(GAME_HEIGHT/2)+TITLE_OFFSET,
            font_name=MESSAGE_FONT,linecolor='white')
        l=super().load_json(DEFAULT_WAVE)
        self._wave=Wave(l)

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game. That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_LOADING,
        STATE_ACTIVE, STATE_PAUSED, and STATE_CONTINUE. Each one of these does its own
        thing, and might even needs its own helper. We describe these below.

        STATE_INACTIVE: This is the state when the application first opens. It is a
        paused state, waiting for the player to start the game. It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key. In addition, the application returns to this state
        when the game is over (all lives are lost or all planetoids are destroyed).

        STATE_LOADING: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay. The player can move the
        ship and fire bullets. All of this should be handled inside of class Wave
        (NOT in this class). Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: Similar to STATE_INACTIVE, state represents the end of
        the app and with no additional animation frames and text showing whether
        the player won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt,int) or isinstance(dt,float)
        if self.input.is_key_pressed('s') and self._state==STATE_INACTIVE:
            self._state=STATE_LOADING
            self._message=None
            self._title=None
            self._state = STATE_ACTIVE
        if self._state==STATE_ACTIVE:
            self._wave.update(dt, self.input)
        self.winlosestates()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. To draw a GObject
        g, simply use the method g.draw(self.view). It is that easy!

        Many of the GObjects (such as the ships, planetoids, and bullets) are attributes
        in Wave. In order to draw them, you either need to add getters for these
        attributes or you need to add a draw method to class Wave. We suggest the latter.
        See the example subcontroller.py from class.
        """
        if self._background != None:
            self._background.draw(self.view)
        if self._wave!=None:
            self._wave.draw(self.view)
        if self._message!=None:
            self._message.draw(self.view)
        if self._title!=None:
            self._title.draw(self.view)
        if self._winlosetext != None:
            self._winlosetext.draw(self.view)

    # HELPER METHODS FOR THE STATES
    def winlosestates(self):
        """
        This method finds if the player won or lost the game and puts a message
        allowing the player to continue to the next wave or retry.

        Parameter self: current instance of the class
        """
        if self._wave.getter_for_winlose() == True:
            if Planetoids.wins < (len(Planetoids.waves) - 1):
                self.winningtext()
                if self.input.is_key_pressed('n'):
                    self.loading()
                    Planetoids.wins+=1
                    if Planetoids.wins <= (len(Planetoids.waves) - 1):
                        l = super().load_json(Planetoids.waves[Planetoids.wins])
                        self._wave=Wave(l)
                        self._state = STATE_ACTIVE
                else:
                    self_state = STATE_COMPLETE
            else:
                self._message = None
                self._title=None
                self._winlosetext = GLabel(text="YOU WIN",
                    font_size=120, x=GAME_WIDTH/2,
                    y=(GAME_HEIGHT/2), font_name=MESSAGE_FONT,linecolor='white')
                self._state=STATE_COMPLETE
        elif self._wave.getter_for_winlose() == False:
            self.losingtext()
            if self.input.is_key_pressed('r'):
                self.loading()
                l = super().load_json(Planetoids.waves[Planetoids.wins])
                self._wave=Wave(l)
                self._state = STATE_ACTIVE
            else:
                self._state = STATE_COMPLETE

    def loading(self):
        """
        This method sets the class into a loading state, changing the message,
        title, and winlosetext attributes.

        Parameter self: current instance of the class
        """
        self._state=STATE_LOADING
        self._message=None
        self._title=None
        self._winlosetext = None

    def winningtext(self):
        """
        This method changes the attributes message and text to reflect that the
        wave was won.

        Parameter self: current instance of the class
        """
        self._winlosetext = GLabel(text="YOU WIN",
            font_size=120, x=GAME_WIDTH/2,
            y=(GAME_HEIGHT/2)+TITLE_OFFSET,
            font_name=MESSAGE_FONT,linecolor='white')
        self._message = GLabel(text="Press n to next wave",
            font_size=MESSAGE_SIZE, x=GAME_WIDTH/2,
            y=(GAME_HEIGHT/2)+MESSAGE_OFFSET,
            font_name=MESSAGE_FONT,linecolor='white')

    def losingtext(self):
        """
        This method changes the attributes message and text to reflect that the
        wave was lost.

        Parameter self: current instance of the class
        """
        self._winlosetext = GLabel(text="YOU LOSE",
            font_size=120, x=GAME_WIDTH/2, y=(GAME_HEIGHT/2)+TITLE_OFFSET,
            font_name=MESSAGE_FONT,linecolor='white')
        self._message = GLabel(text="Press r to retry",
            font_size=MESSAGE_SIZE, x=GAME_WIDTH/2,
            y=(GAME_HEIGHT/2)+MESSAGE_OFFSET,
            font_name=MESSAGE_FONT,linecolor='white')
