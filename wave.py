"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in
the Planetoids game. Instances of Wave represent a single level, and should
correspond to a JSON file in the Data directory. Whenever you move to a new
level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on
screen. These are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue. If you do not know, ask on Ed Discussions and we will answer.

Emily Wei (ejw235) and Amira Razack (arr258)
12/11/24

"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object): #new object
    """
    This class controls a single level or wave of Planetoids.

    This subcontroller has a reference to the ship, asteroids, and any bullets
    on screen. It animates all of these by adding the velocity to the position
    at each step. It checks for collisions between bullets and asteroids or
    asteroids and the ship (asteroids can safely pass through each other). A
    bullet collision either breaks up or removes a asteroid. A ship collision
    kills the player.

    The player wins once all asteroids are destroyed. The player loses if they
    run out of lives. When the wave is complete, you should create a NEW instance
    of Wave (in Planetoids) if you want to make a new wave of asteroids.

    If you want to pause the game, tell this controller to draw, but do not
    update. See subcontrollers.py from Lecture 25 for an example. This class
    will be similar to than one in many ways.

    All attributes of this class are to be hidden. No attribute should be
    accessed without going through a getter/setter first. However, just because
    you have an attribute does not mean that you have to have a getter for it.
    For example, the Planetoids app probably never needs to access the attribute
    for the bullets, so there is no need for a getter there. But at a minimum,
    you need getters indicating whether you one or lost the game.

    CLASS ATTRIBUTES
    Attribute finalship_x = the final position x of the ship when it collides
    with an asteroids
    Invariant: finalship_x is either an int or float that is initially 0

    Attribute finalship_y = the final position y of the ship when it collides
    with an asteroids
    Invariant: finalship_y is either an int or float that is initially 0
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    finalship_x = 0
    finalship_y = 0
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    #
    # Attribute _firerate: the number of frames until the player can fire again
    # Invariant: _firerate is an int >= 0
    #
    # Attribute _winlose: whether or not the wave is won or lost
    # Invariant: _winlose is a boolean either True or False
    #
    # Attribute _bulletsound: a sound for when the bullet is shot
    # Invariant: _bulletsound is a Sound object
    #
    # Attribute _shipsound: a sound for when the ship collides with an asteroid
    # Invariant: _shipsound is a Sound object
    #
    # Attribute _explosion: an explosion animation for when the ship collides
    #           with an asteroid
    # Invariant: _explosion is a GSprite object
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getter_for_winlose(self):
        """
        This method is a getter for whether the wave is won or lost.

        Parameter self: current instance of the class

        self.winlose: A boolean that is either True for a win, and False for a
        loss.
        """
        return self._winlose

    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self,l):
        """
        Initializes a ship and list of asteroids  with its attributes, the
        bullets lists, sounds, and sprite.

        Parameter self: current instance of the class

        Parameter l: current wave json
        Precondition: l is a loaded json dict file
        """
        assert isinstance(l,dict)
        self._data=l
        position=self._data['ship']['position']
        angle=self._data['ship']['angle']
        self._ship=Ship(position,angle)
        self._asteroids = []
        numas = len(self._data['asteroids'])
        for x in range(numas):
            assize = self._data['asteroids'][x]['size']
            asposition = self._data['asteroids'][x]['position']
            asdirection = self._data['asteroids'][x]['direction']
            self._asteroids.append(Asteroid(assize, asposition, asdirection))
        self._bullets = []
        self._firerate = 0
        self._winlose = None
        self._bulletsound = Sound('pew1.wav')
        self._shipsound = Sound('explosion.wav')
        self._explosion = GSprite(x=self._ship.x,y=self._ship.y,
            source='explosion.png',width=2*SHIP_RADIUS,
            height=2*SHIP_RADIUS,format=(2,4),count=8)

    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self,dt,input):
        """
        This method updates the game frames to move the ship, asteroids, and
        bullets as well as show if the player won or lost at the end of the game.

        Parameter: self- the instance of the class

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter: input
        Precondition: input is an instance of GInput
        """
        assert isinstance(dt, int) or isinstance(dt,float)
        assert isinstance(input, GInput)
        if self._ship != None:
            self._firerate += 1
            if self._winlose==None:
                self.inputs(input)
                for bullet in self._bullets:
                    bullet.x += bullet.getter_for_velocity().x
                    bullet.y += bullet.getter_for_velocity().y
                self.wrapthebullets()
                self.shipwrapping()
                self.asteroid_wrapping_and_collisions()
                if self._asteroids == []:
                    self._winlose = True
        else:
            self._winlose = False

    def inputs(self, input):
        """
        This method checks the user's key input to turn the ship, change
        the ship's velocity, and fire bullets when using the specific key
        associated with the action.

        Parameter: self- the instance of the class

        Parameter: input
        Precondition: input is an instance of GInput
        """
        assert isinstance(input, GInput)
        if input.is_key_down('left'):
            self._ship.angle += SHIP_TURN_RATE
            self._ship.turn(self._ship.angle)
        if input.is_key_down('right'):
            self._ship.angle -= SHIP_TURN_RATE
            self._ship.turn(self._ship.angle)
        if input.is_key_down('up'):
            impulse=self._ship.getter_for_impulse()
            self._ship._velocity += impulse
        if input.is_key_down('spacebar') and self._firerate>=BULLET_RATE:
            facing = self._ship.getter_for_facing()
            bullet_posx = facing.x*SHIP_RADIUS+self._ship.x
            bullet_posy = facing.y*SHIP_RADIUS+self._ship.y
            self._bullets.append(Bullet([bullet_posx,bullet_posy],
                self._ship.getter_for_facing()))
            self._firerate = 0
            self._bulletsound.play()

    def wrapthebullets(self):
        """
        This method goes through the self._bullets list and wraps their movement
        on the screen.

        Parameter: self- current instance of the class

        i: The increment counter over the self._bullets list.

        DEAD_ZONE: The area outside of the bounds of the game screen that
        helps wrap the movement of items on the screen.

        GAME_WIDTH: The integer representing the width of the game screen.
        GAME_HEIGHT: The integer representing the height of the game screen.
        """
        i = 0
        while i < len(self._bullets):
            if (self._bullets[i].x < -DEAD_ZONE):
                del self._bullets[i]
            elif (self._bullets[i].y < -DEAD_ZONE):
                del self._bullets[i]
            elif (self._bullets[i].x > GAME_WIDTH+DEAD_ZONE):
                del self._bullets[i]
            elif (self._bullets[i].y > GAME_HEIGHT+DEAD_ZONE):
                del self._bullets[i]
            else:
                i += 1

    def shipwrapping(self):
        """
        This method checks if the ship's speed is too high and
        wraps the ships movement on the screen.

        Parameter: self- the instance of the class

        SHIP_MAX_SPEED: The maximum speed the ship can have.

        GAME_WIDTH: The integer representing the width of the game screen.
        GAME_HEIGHT: The integer representing the height of the game screen.

        DEAD_ZONE: The area outside of the bounds of the game screen that
        helps wrap the movement of items on the screen.

        self._ship: The ship object.

        self._ship._velocity: The vector for the ship's velocity.

        self._ship.x: The x position of the ship.
        self._ship.y: The y position of the ship.

        self._ship.right: The right edge of the ship object.
        self._ship.top: The top edge of the ship object.
        self._ship.left: The left edge of the ship object.
        self._ship.bottom: The bottom edge of the ship object.
        """
        if self._ship._velocity.length() > SHIP_MAX_SPEED:
            normalized=self._ship._velocity.normalize()
            multiplied=normalized.__mul__(SHIP_MAX_SPEED)
            self._ship._velocity=multiplied
        self._ship.x+=self._ship._velocity.x
        self._ship.y+=self._ship._velocity.y
        if (self._ship.right < -DEAD_ZONE):
            self._ship.right = GAME_WIDTH+DEAD_ZONE
        if (self._ship.top < -DEAD_ZONE):
            self._ship.bottom = GAME_HEIGHT+DEAD_ZONE
        if (self._ship.left > GAME_WIDTH+DEAD_ZONE):
            self._ship.right = -DEAD_ZONE
        if (self._ship.bottom > GAME_HEIGHT+DEAD_ZONE):
            self._ship.top = -DEAD_ZONE

    def asteroid_wrapping_and_collisions(self):
        """
        This method checks if the ship's speed is too high and
        wraps the ships movement on the screen.

        Parameter: self- the instance of the class

        GAME_WIDTH: The integer representing the width of the game screen.
        GAME_HEIGHT: The integer representing the height of the game screen.

        DEAD_ZONE: The area outside of the bounds of the game screen that
        helps wrap the movement of items on the screen.

        ast: The increment counter for a single asteroid in self._asteroids.

        self._asteroids[ast]: An individual asteroid object in self._asteroids.

        self._ship: The GImage ship object.

        self.shipsound: The wav sound of the ship.

        bullet: The increment counter for the list of self._bullets

        self._bullets: The list of bullet objects in the game.

        bluh: The three Vector2 resultant vectors calculated for the medium or
        large asteroid.
        """
        ast=0
        while ast < len(self._asteroids):
            self._asteroids[ast].x += self._asteroids[ast]._velocity.x
            self._asteroids[ast].y += self._asteroids[ast]._velocity.y
            self.asteroid_wrap(ast)
            if (self._ship != None):
                if self._ship.isCollided(self._asteroids[ast]):
                    Wave.finalship_x = self._ship.x
                    Wave.finalship_y = self._ship.y
                    self._ship = None
                    self._shipsound.play()
            bullet=0
            while bullet < len(self._bullets):
                if ast in range(len(self._asteroids)):
                    asteroidd=self._asteroids[ast]
                if self._bullets[bullet].bullet_isCollided(asteroidd):
                    self._bullets.remove(self._bullets[bullet])
                    size = asteroidd.get_size()
                    if size=='medium' or size=='large':
                        bluh=asteroidd.resultant_vectors()
                        self.place_asteroids(asteroidd.get_size(),bluh,ast)
                        del self._asteroids[ast]
                    elif size=='small':
                        del self._asteroids[ast]
                else:
                    bullet+=1
            if ast < len(self._asteroids):
                ast+=1

    def asteroid_wrap(self,ast):
        """
        This method wraps the movement of the asteroids on the screen.

        Parameter: self- current instance of the class

        Parameter: ast
        Precondition: An integer between 0 and the length of self._asteroids

        DEAD_ZONE: The area outside of the bounds of the game screen that
        helps wrap the movement of items on the screen.

        GAME_WIDTH: The integer representing the width of the game screen.
        GAME_HEIGHT: The integer representing the height of the game screen.
        """
        if (self._asteroids[ast].right < -DEAD_ZONE):
            self._asteroids[ast].right = GAME_WIDTH+DEAD_ZONE
        if (self._asteroids[ast].top < -DEAD_ZONE):
            self._asteroids[ast].bottom = GAME_HEIGHT+DEAD_ZONE
        if (self._asteroids[ast].left > GAME_WIDTH+DEAD_ZONE):
            self._asteroids[ast].right = -DEAD_ZONE
        if (self._asteroids[ast].bottom > GAME_HEIGHT+DEAD_ZONE):
            self._asteroids[ast].top = -DEAD_ZONE

    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self,view):
        """
        The draw method to draw the ship, asteroid, and bullets.

        Parameter: view
        Precondition: is an instance of GView

        self._ship: The ship object
        self._asteroids: The asteroid objects in the game.
        self._bullets: The bullet objects in the game.
        """
        assert isinstance(view, GView)
        if self._ship != None:
            self._ship.draw(view)
            for x in range(len(self._bullets)):
                self._bullets[x].draw(view)
        else:
            if self._explosion != None:
                self._explosion.x = Wave.finalship_x
                self._explosion.y = Wave.finalship_y
                self._explosion.draw(view)
                if self._explosion.frame < self._explosion.count-1:
                    self._explosion.frame += 1
                if self._explosion.frame == self._explosion.count-1:
                    self._explosion = None
        for x in range(len(self._asteroids)):
            self._asteroids[x].draw(view)
        if self._asteroids == [] and self._winlose == True:
            self._bullets = []
            self._ship.draw(view)

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def place_asteroids(self,size,bluh,ast):
        """
        This method creates three asteroids when medium and large asteroids
        break up.

        Parameter self: current instance of the class

        Parameter: size
        Precondition: A string that is either 'medium' or 'large'

        Parameter: bluh
        Precondition: A list of three Vector2 resultant vectors for an asteroid
        in self._asteroids

        Parameter: ast
        Precondition: An integer between 0 and the length of self._asteroids

        self._ship: The ship object
        self._asteroids: The asteroid objects in the game.
        self._bullets: The bullet objects in the game.

        posx: List for the relative x coordinates of a stationary asteroid.
        posy: List for the relative y coordinates of a stationary asteroid.

        velocity: The velocity of the new asteroid.
        newposition: The new asteroid's x and y coordinates.

        SMALL_RADIUS: The small asteroid radius value from consts.py
        MEDIUM_RADIUS: The medium asteroid radius value from consts.py

        SMALL_SPEED: The small asteroid speed value from consts.py
        MEDIUM_SPEED: The medium asteroid speed value from consts.py

        self._asteroids[ast]: The individual asteroid that the calculations
        are being performed on.
        """
        assert isinstance(ast,int) and ast in range(len(self._asteroids))
        posx=[1,-1,0]
        posy=[1, 1,-1]
        if size=='medium':
            for i in range(3):
                velocity=bluh[i]*SMALL_SPEED
                if velocity.x==0.0 and velocity.y==0.0:
                    newposition=(SMALL_RADIUS*posx[i]+self._asteroids[ast].x,
                        SMALL_RADIUS*posy[i]+self._asteroids[ast].y)
                else:
                    newposition=(SMALL_RADIUS*bluh[i].x+self._asteroids[ast].x,
                        SMALL_RADIUS*bluh[i].y+self._asteroids[ast].y)
                self._asteroids.append(Asteroid('small',newposition,velocity))
        elif size=='large':
            for i in range(3):
                velocity=bluh[i]*MEDIUM_SPEED
                if velocity.x==0.0 and velocity.y==0.0:
                    newposition=(MEDIUM_RADIUS*posx[i]+self._asteroids[ast].x,
                        MEDIUM_RADIUS*posy[i]+self._asteroids[ast].y)
                else:
                    newposition=(MEDIUM_RADIUS*bluh[i].x+self._asteroids[ast].x,
                        MEDIUM_RADIUS*bluh[i].y+self._asteroids[ast].y)
                self._asteroids.append(Asteroid('medium',newposition,velocity))
