"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that
you interact with on the screen is model: the ship, the bullets, and the
planetoids.

We need models for these objects because they contain information beyond the
simple shapes like GImage and GEllipse. In particular, ALL of these classes
need a velocity representing their movement direction and speed (and hence they
all need an additional attribute representing this fact). But for the most part,
that is all they need. You will only need more complex models if you are adding
advanced features like scoring.

You are free to add even more models to this module. You may wish to do this
when you add new features to your game, such as power-ups. If you are unsure
about whether to make a new class or not, please ask on Ed Discussions.

Emily Wei (ejw235) and Amira Razack (arr258)
12/11/24

"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a
# parameter in your method, and Wave should pass it as a argument when it calls
# the method.


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship

    Bullets are typically just white circles (ellipses). The size of the bullet
    is determined by constants in consts.py. However, we MUST subclass GEllipse,
    because we need to add an extra attribute for the velocity of the bullet.

    The class Wave will need to look at this velocity, so you will need getters
    for the velocity components. However, it is possible to write this assignment
    with no setters for the velocities. That is because the velocity is fixed
    and cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set the
    starting velocity. This __init__ method will need to call the __init__ from
    GEllipse as a helper. This init will need a parameter to set the direction
    of the velocity.

    You also want to create a method to update the bolt. You update the bolt by
    adding the velocity to the position. While it is okay to add a method to
    detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _velocity: the direction and speed the bullet is traveling
    # Invariant: _velocity is a Vector2 object and objects of this class represent a 2D vector

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getter_for_velocity(self):
        """
        This method is a getter for the velocity of the bullet.

        Parameter self: current instance of the class

        self._velocity: The velocity vector of the bullet velocity.
        """
        return self._velocity

    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, position, direction):
        """
        Initializes the position, size, color, and velocity of a bullet.

        Parameter position: the x and y coordinates of the location of the
        bullet.
        Precondition: position is a list of ints or floats with a length of 2

        Parameter direction: the direction of the bullet based on the ships
        facing angle
        Precondition: direction is a Vector2 object
        """
        assert isinstance(position,list) and len(position) == 2
        assert isinstance(position[0],int) or isinstance(position[0],float)
        assert isinstance(position[1],int) or isinstance(position[1],float)
        assert isinstance(direction,Vector2)
        super().__init__(x=position[0],y=position[1],width=2*BULLET_RADIUS,
            height=2*BULLET_RADIUS,fillcolor=BULLET_COLOR)
        velocity_x = direction.x * BULLET_SPEED
        velocity_y = direction.y * BULLET_SPEED
        self._velocity = Vector2(velocity_x, velocity_y)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def dist_between_center(self, asteroid):
        """
        This method returns the distance between the center of the bullet and
        asteroid.

        Parameter self: current instance of the class
        Parameter asteroid: any Asteroid object
        Precondition: asteroid is an Asteroid object
        """
        assert isinstance(asteroid,Asteroid)
        return Point2.distance(Point2(self.x,self.y),Point2(asteroid.getter_x(),
             asteroid.getter_y()))

    def bullet_isCollided(self, asteroid):
        """
        This method returns whether or not a bullet has collided with an
        asteroid using the dist_between_center() helper function.

        Parameter self: current instance of the class
        Parameter asteroid: an Asteroid object that is either overlapping or not
        with the bullet
        Precondition: asteroid is an Asteroid object
        """
        assert isinstance(asteroid, Asteroid)
        sum_radii = BULLET_RADIUS + (asteroid.getter_width() / 2)
        if self.dist_between_center(asteroid) < sum_radii:
            return True
        else:
            return False


class Ship(GImage):
    """
    A class to represent the game ship.

    This ship is represented by an image. The size of the ship is determined by
    constants in consts.py. However, we MUST subclass GEllipse, because we need
    to add an extra attribute for the velocity of the ship, as well as the facing
    vector (not the same) thing.

    The class Wave will need to access these two values, so you will need getters
    for them. But per the instructions,these values are changed indirectly by
    applying thrust or turning the ship. That means you won't want setters for
    these attributes, but you will want methods to apply thrust or turn the ship.

    This class needs an __init__ method to set the position and initial facing
    angle. This information is provided by the wave JSON file. Ships should
    start with a shield enabled.

    Finally, you want a method to update the ship. When you update the ship, you
    apply the velocity to the position. While it is okay to add a method to
    detect collisions in this class, you may find it easier to process collisions
    in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _velocity: the direction and speed the ship is traveling
    # Invariant: _velocity is a Vector2 object and objects of this class represent a 2D vector
    #
    # Attribute _facing: the direction the ship is facing
    # Invariant: _wave is a Vector2 object and objects of this class represent a 2D vector

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getter_for_impulse(self):
        """
        This method is the getter for the ship's impulse.

        Parameter self: current instance of the class

        self._facing: The vector for the direction the ship is facing.
        SHIP_IMPULSE: The ship's change in momentum constant
        found in consts.py.
        """
        return self._facing.__mul__(SHIP_IMPULSE)

    def getter_for_facing(self):
        """
        This method is the getter for the ship's direction value.

        Parameter self: current instance of the class

        self._facing: The vector for the direction the ship is facing.
        """
        return self._facing

    def get_theta(self, angle):
        """
        This method returns the unit vector using the value of theta
        converted from degrees to radians.

        Parameter self: current instance of the class

        Parameter: angle
        Precondition: angle can be any number

        theta: The angle converted to radians.
        """
        assert isinstance(angle,int) or isinstance(angle,float)
        theta=angle * (math.pi/180)
        return Vector2(math.cos(theta),math.sin(theta))

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,position,angle):
        """
        Initializes the position, size, facing angle, and velocity of a ship.

        Parameter position: the x and y coordinates of the location of the
        ship.
        Precondition: position is a list of ints or floats with a length of 2

        Parameter angle: the angle of the ship in degrees
        Precondition: angle is any number
        """
        assert isinstance(position,list) and len(position) == 2
        assert isinstance(position[0],int) or isinstance(position[0],float)
        assert isinstance(position[1],int) or isinstance(position[1],float)
        assert isinstance(angle,float) or isinstance(angle,int)
        super().__init__(x=position[0],y=position[1],width=2*SHIP_RADIUS,height=
            2*SHIP_RADIUS,source=SHIP_IMAGE)
        self.angle=angle
        self._velocity=Vector2(0,0)
        self._facing=self.get_theta(self.angle)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self,angle):
        """
        This method updates the angle and facing vector.

        Parameter self: current instance of the class

        Parameterangle: how much the ship is rotated
        Precondition: angle can be any number

        theta: The angle converted to radians.

        self._facing: The vector for the direction that the ship is facing.
        """
        assert isinstance(angle, int) or isinstance(angle, float)
        self.angle=angle
        theta=self.angle*(math.pi/180)
        self._facing=Vector2(math.cos(theta),math.sin(theta))

    def dist_between_center(self, asteroid):
        """
        This method returns the distance between the centers of the asteroid
        and ship object.

        Parameter self: current instance of the class

        Parameter: an asteroid
        Precondition: asteroid is a single GImage Asteroid object
        """
        assert isinstance(asteroid,Asteroid)
        return Point2.distance(Point2(self.x,self.y),Point2(asteroid.getter_x(),
             asteroid.getter_y()))

    def isCollided(self, asteroid):
        """
        This method returns True if the distance between the two centers of
        the ship and asteroid was less than their combined radii and False
        if the distance was greater.

        Parameter self: current instance of the class

        Parameter: an asteroid
        Precondition: asteroid is a single GImage Asteroid object

        sum_radii: The sum of the ship radius constant in consts.py and
        the radius of the asteroid.

        SHIP_RADIUS: The ship radius constant from consts.py.
        """
        assert isinstance(asteroid, Asteroid)
        sum_radii = SHIP_RADIUS + (asteroid.getter_width() / 2)
        if self.dist_between_center(asteroid) < sum_radii:
            return True
        else:
            return False


class Asteroid(GImage):
    """
    A class to represent a single asteroid.

    Asteroids are typically are represented by images. Asteroids come in three
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that
    determine the choice of image and asteroid radius. We MUST subclass GImage,
    because we need extra attributes for both the size and the velocity of the
    asteroid.

    The class Wave will need to look at the size and velocity, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for either of these. That is because they are fixed and cannot
    change when the asteroid is created.

    In addition to the getters, you need to write the __init__ method to set the
    size and starting velocity. Note that the SPEED of an asteroid is defined in
    const.py, so the only thing that differs is the velocity direction.

    You also want to create a method to update the asteroid. You update the
    asteroid by adding the velocity to the position. While it is okay to add a
    method to detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _velocity: the direction and speed the asteroid is travelling
    # Invariant: _velocity is a Vector2 object and objects of this class represent a 2D vector

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_velocity(self):
        """
        This method is a getter for the velocity of the asteroid.

        Parameter self: current instance of the class

        self._velocity: The velocity vector of the asteroid.
        """
        return self._velocity

    def get_size(self):
        """
        This method is a getter for the size of the asteroid and returns
        the categorization of the asteroid's size.

        Parameter self: current instance of the class

        self.width: The width of the entire asteroid.

        SMALL_RADIUS: The radius of the small asteroid found in consts.py.
        MEDIUM_RADIUS: The radium of the medium asteroid found in consts.py
        """
        if (self.width == 2*SMALL_RADIUS):
            return 'small'
        elif (self.width == 2*MEDIUM_RADIUS):
            return 'medium'
        else:
            return 'large'

    def getter_x(self):
        """
        This method is a getter for the x position of the asteroid.

        Parameter self: current instance of the class

        self.x: The x position of the asteroid.
        """
        return self.x

    def getter_y(self):
        """
        This method is a getter for the y position of the asteroid.

        Parameter self: current instance of the class

        self.y: The y position of the asteroid.
        """
        return self.y

    def getter_width(self):
        """
        This method is a getter for width of the asteroid.

        Parameter self: current instance of the class

        self.width: The width of the entire asteroid.
        """
        return self.width

    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, size, position, direction):
        """
        Initializes the position, size, direction, image, and velocity of an
        asteroid.

        Parameter size: either "small", "medium", or "large"
        Precondition: size is a string

        Parameter position: the x and y coordinates of the location of the
        asteroid.
        Precondition: position is a list or tuple of ints or floats with a
        length of 2

        Parameter direction: direction angle of an asteroid
        Precondition: direction is either a list or a Vector2 object
        """
        assert isinstance(position[0],int) or isinstance(position[0],float)
        assert isinstance(position[1],int) or isinstance(position[1],float)
        assert isinstance(size,str) and len(position) == 2
        assert isinstance(direction, list) or isinstance(direction, Vector2)
        zero_vector = Vector2(0,0)
        if isinstance(direction, list):
            direction_vect = Vector2(direction[0],direction[1])
        elif isinstance(direction, Vector2):
            direction_vect = Vector2(direction.x,direction.y)
        if (size == 'small'):
            super().__init__(x=position[0],y=position[1],width=2*SMALL_RADIUS,
                height=2*SMALL_RADIUS,source=SMALL_IMAGE)
            if (direction_vect.__eq__(zero_vector)):
                self._velocity = zero_vector
            else:
                self._velocity=direction_vect.normalize().__mul__(SMALL_SPEED)
        if (size == 'medium'):
            super().__init__(x=position[0],y=position[1],width=2*MEDIUM_RADIUS,
                height=2*MEDIUM_RADIUS,source=MEDIUM_IMAGE)
            if (direction_vect.__eq__(zero_vector)):
                self._velocity = zero_vector
            else:
                self._velocity=direction_vect.normalize().__mul__(MEDIUM_SPEED)
        if (size == 'large'):
            super().__init__(x=position[0],y=position[1],width=2*LARGE_RADIUS,
                height=2*LARGE_RADIUS,source=LARGE_IMAGE)
            if (direction_vect.__eq__(zero_vector)):
                self._velocity = zero_vector
            else:
                self._velocity=direction_vect.normalize().__mul__(LARGE_SPEED)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def resultant_vectors(self):
        """
        This method creates three asteroids when medium and large asteroids
        break up.

        Parameter self: current instance of the class

        angle: Starting angle of 120 that is incremented by 120 to produce three
        asteroids with different angles.

        vx: The x position of the velocity vector.
        vy: The y position of the velocity vector.

        listi: A list of the three resultant vectors that is returned.
        """
        vx=self._velocity.x
        vy=self._velocity.y
        listi=[]
        angle=120
        for i in range(3):
            if vx==0.0 and vy==0.0:
                listi.append(Vector2(0,0))
            else:
                listi.append(Vector2(vx*math.cos(math.radians(angle))-vy*
                    math.sin(math.radians(angle)),
                    vx*math.sin(math.radians(angle))+vy*math.cos
                    (math.radians(angle))).normalize())
            angle+=120
        return listi
