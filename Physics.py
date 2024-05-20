import phylib;
import sqlite3;
import os
import math
import random
from xml.etree import ElementTree as ET

################################################################################
# import constants from phylib to global variables
BALL_RADIUS    = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER  = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS    = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH   = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH    = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE       = phylib.PHYLIB_SIM_RATE
VEL_EPSILON    = phylib.PHYLIB_VEL_EPSILON
DRAG           = phylib.PHYLIB_DRAG
MAX_TIME       = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS    = phylib.PHYLIB_MAX_OBJECTS
FRAME_INTERVAL = 0.01

# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="table-svg" class="rotate-image" width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n"""

HEADER_NO_RECT = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "GOLD",
    "BLUE",
    "RED",
    "PURPLE",
    "DARKORANGE",
    "GREEN",
    "SADDLEBROWN",
    "BLACK",
    "YELLOW",
    "DEEPSKYBLUE",
    "MAGENTA",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "SANDYBROWN",      # no LIGHTORANGE
    "LAWNGREEN",
    "CHOCOLATE",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall

    #Figure out how to assign correct ball colour based on index (hardcoded right now)
    def svg(self):
        if self.obj.still_ball.number == 0:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="cueBall"/>\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        else:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="%d"/>\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number], self.obj.still_ball.number)

class RollingBall( phylib.phylib_object ):
    #Python RollingBall class.

    def __init__(self, number, pos, vel, acc):
        #Constructor

        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_ROLLING_BALL,
            number,
            pos,
            vel,
            acc,
            0.0,
            0.0
        )

        self.__class__ = RollingBall

    def svg(self):
        if self.obj.rolling_ball.number == 0:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="cueBall"/>\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        else:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="%d"/>\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number], self.obj.rolling_ball.number)


class Hole(phylib.phylib_object):
    #Python Hole class.

    def __init__(self, pos):
        #Constructor

        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_HOLE,
            None,
            pos,
            None,
            None,
            0.0,
            0.0
        )

        self.__class__ = Hole

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)


class HCushion(phylib.phylib_object):
    #Python HCushion class.

    def __init__(self, y):
        #Constructor

        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_HCUSHION, 
            None,
            None,
            None,
            None,
            0.0,
            y
        )

        self.__class__ = HCushion

    def svg(self):
        if (self.obj.hcushion.y == 0.0):
            return """ <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            return """ <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />\n"""


class VCushion(phylib.phylib_object):
    #Python VCushion class.

    def __init__(self, x):
        #Constructor

        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_VCUSHION,
            None,
            None,
            None,
            None,
            x,
            0.0
        )

        self.__class__ = VCushion

    def svg(self):
        if (self.obj.vcushion.x == 0.0):
            return """ <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            return """ <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />\n"""


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.2f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    #Table svg function
    #creates svg filenames for all objects in table
    def svg(self):
        string = HEADER
        
        i = 0
        for object in self:
            if self[i]:
                string += self[i].svg()
            i += 1
                
        string += FOOTER
        return string
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                Coordinate(0,0),
                Coordinate(0,0),
                Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall(self):
        for i in self:
            if (type(i) == StillBall and i.obj.still_ball.number == 0) or (type(i) == RollingBall and i.obj.rolling_ball.number == 0):
                return i

    def nudge(self):
        return random.uniform( -1.5, 1.5 );

    def startingTable(self):
        
        # self += StillBall(0, Coordinate(TABLE_WIDTH / 2.0, TABLE_LENGTH - TABLE_WIDTH / 2.0))
        # self += StillBall(1, Coordinate(TABLE_WIDTH / 2.0, TABLE_WIDTH / 2.0 + BALL_DIAMETER))
        # self += StillBall(2, Coordinate(TABLE_WIDTH / 2.0 - (BALL_DIAMETER + 4.0) / 2.0 + self.nudge(), TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) + BALL_DIAMETER + self.nudge()))
        # self += StillBall(3, Coordinate(TABLE_WIDTH / 2.0 + (BALL_DIAMETER + 4.0) / 2.0 + self.nudge(), TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) + BALL_DIAMETER + self.nudge()))
        # self += StillBall(4, Coordinate(TABLE_WIDTH / 2.0 - (BALL_DIAMETER + 4.0) / 2.0 + self.nudge() - 0.5 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) + self.nudge()))
        # self += StillBall(5, Coordinate(TABLE_WIDTH / 2.0, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) + self.nudge()))
        # self += StillBall(6, Coordinate(TABLE_WIDTH / 2.0 + (BALL_DIAMETER + 4.0) / 2.0 + self.nudge() + 0.5 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) + self.nudge()))
        # self += StillBall(7, Coordinate(TABLE_WIDTH / 2.0 - (BALL_DIAMETER + 12.0) / 2.0 + self.nudge() - 1.0 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - BALL_DIAMETER + self.nudge()))
        # self += StillBall(8, Coordinate(TABLE_WIDTH / 2.0 - (BALL_DIAMETER + 4.0) / 2.0 + self.nudge(), TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - BALL_DIAMETER + self.nudge()))
        # self += StillBall(9, Coordinate(TABLE_WIDTH / 2.0 + (BALL_DIAMETER + 4.0) / 2.0 + self.nudge(), TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - BALL_DIAMETER + self.nudge()))
        # self += StillBall(10, Coordinate(TABLE_WIDTH / 2.0 + (BALL_DIAMETER + 4.0) / 2.0 + self.nudge() + 1.0 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - BALL_DIAMETER + self.nudge()))
        # self += StillBall(11, Coordinate(TABLE_WIDTH / 2.0 - (BALL_DIAMETER + 12.0) / 2.0 + self.nudge() - 1.5 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - 2.0 * BALL_DIAMETER + self.nudge()))
        # self += StillBall(12, Coordinate(TABLE_WIDTH / 2.0 - (BALL_DIAMETER + 4.0) / 2.0 + self.nudge() - 0.5 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - 2.0 * BALL_DIAMETER + self.nudge()))
        # self += StillBall(13, Coordinate(TABLE_WIDTH / 2.0, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - 2.0 * BALL_DIAMETER + self.nudge()))
        # self += StillBall(14, Coordinate(TABLE_WIDTH / 2.0 + (BALL_DIAMETER + 4.0) / 2.0 + self.nudge() + 0.5 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - 2.0 * BALL_DIAMETER + self.nudge()))
        # self += StillBall(15, Coordinate(TABLE_WIDTH / 2.0 + (BALL_DIAMETER + 16.0) / 2.0 + self.nudge() + 1.5 * BALL_DIAMETER, TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) - 2.0 * BALL_DIAMETER + self.nudge()))

        # Positions that are proven to work. Can use these instead of above
        self += StillBall(0, Coordinate(TABLE_WIDTH / 2.0, TABLE_LENGTH - TABLE_WIDTH / 2.0))
        self += StillBall(1, Coordinate(675.0, 732.0))
        self += StillBall(2, Coordinate(645.5, 678.0))
        self += StillBall(3, Coordinate(705.2, 678.0))
        self += StillBall(4, Coordinate(615.5, 621.5))
        self += StillBall(5, Coordinate(675.0, 622.9))
        self += StillBall(6, Coordinate(734.9, 621.1))
        self += StillBall(7, Coordinate(583.1, 566.5))
        self += StillBall(8, Coordinate(645.7, 563.9))
        self += StillBall(9, Coordinate(705.8, 565.0))
        self += StillBall(10, Coordinate(763.5, 565.2))
        self += StillBall(11, Coordinate(556.2, 508.5))
        self += StillBall(12, Coordinate(614.7, 507.2))
        self += StillBall(13, Coordinate(675.0, 509.4))
        self += StillBall(14, Coordinate(735.0, 507.4))
        self += StillBall(15, Coordinate(795.9, 507.6))

    def readSvg(self, filename):
        fp = open(filename)
        content = fp.read()

        root = ET.fromstring(content)

        # if os.path.exists("reference.svg"):
        #     os.remove("reference.svg")
        # fp = open("reference.svg", "w")
        # fp.write(content)

        circles = root.findall('{http://www.w3.org/2000/svg}circle')

        for circle in circles:
            if float(circle.get('r')) == 28:
                cx = float(circle.get('cx'))
                cy = float(circle.get('cy'))
                r = float(circle.get('r'))
                num = circle.get('id')
                if num == 'cueBall':
                    ball_number = 0
                else:
                    ball_number = int(num)

                ball = StillBall(ball_number, Coordinate(cx, cy))
                self += ball
        


class Database():
    conn = None
    def __init__(self, reset = False):
        if reset == True and os.path.exists('phylib.db'):
            os.remove('phylib.db')
        self.conn = sqlite3.connect('phylib.db')

    def createDB(self):
        cur = self.conn.cursor()
        #Remember to call close() and commit()

        #Create Ball table
        
        cur.execute(
            #Removed AUTO_INCREMENT (not necessary?)
            """CREATE TABLE IF NOT EXISTS Ball
                (BALLID     INTEGER NOT NULL, 
                 BALLNO     INTEGER NOT NULL,
                 XPOS       FLOAT NOT NULL,
                 YPOS       FLOAT NOT NULL,
                 XVEL       FLOAT,
                 YVEL       FLOAT,
                 PRIMARY KEY (BALLID));"""
        )

        #Create TTable table
        cur.execute(
            #Removed AUTO_INCREMENT (not necessary?)
            """CREATE TABLE IF NOT EXISTS TTable
                (TABLEID    INTEGER NOT NULL,
                 TIME       FLOAT NOT NULL,
                 PRIMARY KEY (TABLEID))"""
        )

        #Create BallTable table
        cur.execute(
            """CREATE TABLE IF NOT EXISTS BallTable
                (BALLID     INTEGER NOT NULL,
                 TABLEID    INTEGER NOT NULL,
                 FOREIGN KEY (BALLID) REFERENCES Ball,
                 FOREIGN KEY (TABLEID) REFERENCES TTable)"""
        )

        #Create Shot table
        cur.execute(
            #Removed AUTO_INCREMENT (not necessary?)
            """CREATE TABLE IF NOT EXISTS Shot
                (SHOTID     INTEGER NOT NULL,
                 PLAYERID   INTEGER NOT NULL,
                 GAMEID     INTEGER NOT NULL,
                 PRIMARY KEY (SHOTID),
                 FOREIGN KEY (GAMEID) REFERENCES Game,
                 FOREIGN KEY (PLAYERID) REFERENCES Player)"""
        )

        #Create TableShot table
        cur.execute(
            """CREATE TABLE IF NOT EXISTS TableShot
                (TABLEID    INTEGER NOT NULL,
                 SHOTID     INTEGER NOT NULL,
                 FOREIGN KEY (TABLEID) REFERENCES TTable,
                 FOREIGN KEY (SHOTID) REFERENCES Shot)"""
        )

        #Create Game table
        cur.execute(
            #Removed AUTO_INCREMENT (not necessary?)
            """CREATE TABLE IF NOT EXISTS Game
                (GAMEID     INTEGER NOT NULL,
                 GAMENAME   VARCHAR(64) NOT NULL,
                 PRIMARY KEY (GAMEID))"""
        )

        #Create Player table
        cur.execute(
            #Removed AUTO_INCREMENT (not necessary?)
            """CREATE TABLE IF NOT EXISTS Player
                (PLAYERID   INTEGER NOT NULL,
                 GAMEID     INTEGER NOT NULL,
                 PLAYERNAME VARCHAR(64) NOT NULL,
                 PRIMARY KEY (PLAYERID),
                 FOREIGN KEY (GAMEID) REFERENCES Game)"""
        )

        cur.close()
        self.conn.commit()

    def readTable(self, tableID):
        table = Table()
        
        cur = self.conn.cursor()

        #Read from BallTable to add balls to table
        cur.execute(
            """SELECT * FROM (Ball INNER JOIN BallTable 
               ON
               Ball.BALLID=BallTable.BALLID)
               WHERE BallTable.TABLEID=?;""", (str(int(tableID) + 1),)
        )
        balls = cur.fetchall()

        cur.execute(
            """SELECT TIME FROM TTable WHERE TABLEID=?""", (str(int(tableID) + 1),))

        time = cur.fetchone()

        if not balls:
            print("no balls for these tables?")
            return None

        ballIDs = []
        
        for i in balls:
            ballIDs.append(i[0]) #Set ballID to column 1 of each ball entry


        #Use ballID to find ball data from Ball table
        for i in range(0, len(balls)):
            
            #Initialize ball as StillBall if vel == 0
            if balls[i][4] == None and balls[i][5] == None:
                newBall = StillBall(
                    balls[i][1],
                    Coordinate(float(balls[i][2]), float(balls[i][3]))    
                )
                table += newBall
            else: #Initialize RolllingBall
                # Calculate RollingBall Acceleration
                rb_dx = float(balls[i][4])
                rb_dy = float(balls[i][5])
                rb_speed = math.sqrt(float((rb_dx * rb_dx) + (rb_dy * rb_dy)))

                rb_acc_x = ((-1.0) * (rb_dx) / rb_speed) * DRAG
                rb_acc_y = ((-1.0) * (rb_dy) / rb_speed) * DRAG

                # Create RollingBall
                newBall = RollingBall(
                    balls[i][1], 
                    Coordinate(float(balls[i][2]), float(balls[i][3])),
                    Coordinate(rb_dx, rb_dy),
                    Coordinate(rb_acc_x, rb_acc_y)
                )
                table += newBall
        if table:
            table.time = time[0]
        #Remember to add shit to the Table object
        #Next get time from TTable
        self.conn.commit()
        cur.close() #see if this works

        return table

    def writeTable(self, table):
        cur = self.conn.cursor()

        #Insert table values into SQL tables

        #Start with time
        cur.execute( # Figure out how to do pass something into the autoincerment
            """INSERT INTO TTable (TIME)
               VALUES ('""" + str(table.time) + """')
            """
        )

        #Get TABLEID
        cur.execute(
            """SELECT * FROM TTable WHERE (TTable.TIME=""" + str(table.time) + """)
            """
        )
        idTable = cur.fetchone()
        tableID = idTable[0] #This is tableID + 1 because SQL

        # Loop through all balls and add to Ball table
        for i in table:
            if type(i) is StillBall:
                cur.execute(
                    """INSERT INTO Ball (BALLNO, XPOS, YPOS)
                       VALUES ('""" + str(i.obj.still_ball.number) + """', 
                               '""" + str(i.obj.still_ball.pos.x) + """', 
                               '""" + str(i.obj.still_ball.pos.y) + """')
                    """
                )
                # Find ballID to insert into BallTable
                ballRowID = cur.lastrowid
                cur.execute(
                    """SELECT * FROM Ball WHERE BALLID = ?""", (ballRowID,)
                )
                temp = cur.fetchone()
                ballID = temp[0]

                # Add to BallTable
                cur.execute(
                    """INSERT INTO BallTable (BALLID, TABLEID)
                       VALUES ('""" + str(ballID) + """',
                               '""" + str(tableID) + """')
                    """
                )
            elif type(i) is RollingBall:
                cur.execute(
                    """INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                       VALUES ('""" + str(i.obj.rolling_ball.number) + """', 
                               '""" + str(i.obj.rolling_ball.pos.x) + """', 
                               '""" + str(i.obj.rolling_ball.pos.y) + """', 
                               '""" + str(i.obj.rolling_ball.vel.x) + """', 
                               '""" + str(i.obj.rolling_ball.vel.y) + """')
                    """
                )
                # Find ballID to insert into BallTable
                ballRowID = cur.lastrowid
                cur.execute(
                    """SELECT * FROM Ball WHERE BALLID = ?""", (ballRowID,)
                )
                temp = cur.fetchone()
                ballID = temp[0]

                # Add to BallTable
                cur.execute(
                    """INSERT INTO BallTable (BALLID, TABLEID)
                       VALUES ('""" + str(ballID) + """',
                               '""" + str(tableID) + """')
                    """
                )

        self.conn.commit()
        cur.close()
        return (tableID - 1)
    
    # Function commits and closes SQL connection
    def close(self):
        self.conn.commit()
        self.conn.close()

    def newShot(self, playerName):
        #helper method for shot function in Game class
        cur = self.conn.cursor()

        cur.execute(
            """SELECT * FROM Player WHERE (Player.PLAYERNAME=?)""", (str(playerName),))
        
        temp = cur.fetchone()
        playerID = temp[0]
        gameID = temp[1]

        cur.execute(
            """INSERT INTO Shot (PLAYERID, GAMEID)
               VALUES (?, ?)""", (playerID, gameID,)
        )

        new_row_id = cur.lastrowid

        cur.execute(
            """SELECT * FROM Shot WHERE SHOTID = ?""", (new_row_id,))
        # obtain shotID and return it to shoot() in Game
        temp = cur.fetchone()
        shotID = temp[0]

        cur.close()
        self.conn.commit()
        return shotID
    
    def update_TableShot(self, table, shotID):
        cur = self.conn.cursor()

        cur.execute(
            """SELECT * FROM TTable WHERE (TTable.TIME=""" + str(table.time) + """)
            """
        )
        temp = cur.fetchone()
        tableID = temp[0]

        cur.execute(
            """INSERT INTO TableShot (TABLEID, SHOTID)
               VALUES ('""" + str(tableID) + """',
                       '""" + str(shotID) + """')
            """
        )

        cur.close()
        self.conn.commit()

    def setGame(self, gameName, player1Name, player2Name):
        cur = self.conn.cursor()

        cur.execute(
            """INSERT INTO Game (GAMENAME)
                VALUES ('""" + str(gameName) + """')
            """
        )
        gameRowID = cur.lastrowid
        cur.execute(
            """SELECT * FROM Game WHERE GAMEID = ?""", (gameRowID,))
        temp = cur.fetchone()
        gameID = temp[0]
        self.gameID = gameID

        print("Gets to inserting players")
        cur.execute(
            """INSERT INTO Player (GAMEID, PLAYERNAME)
                VALUES (?, ?)""", (str(gameID), str(player1Name))
        )

        cur.execute(
            """INSERT INTO Player (GAMEID, PLAYERNAME)
                VALUES ('""" + str(gameID) + """',
                        '""" + str(player1Name) + """')
            """
        )

        cur.execute(
            """INSERT INTO Player (GAMEID, PLAYERNAME)
                VALUES (?, ?)""", (str(gameID), str(player2Name))
        )
        cur.close()
        self.conn.commit()


class Game():
    gameID = None
    gameName = None
    player1Name = None
    player2Name = None
    def __init__(self, gameID = None, gameName = None, player1Name = None, player2Name = None):
        try:
            if type(gameID) != int:
                if type(gameName) != str or type(player1Name) != str or type(player2Name) != str:
                    raise TypeError

            elif type(gameName) is not None or type(player1Name) is not None or type(player2Name) is not None:
                raise TypeError
            
            if type(gameID) == int:
                #Constructor 1
                gameID += 1

                #Retrieve values from database
                #gameName, player1Name, player2Name
                cur = self.conn.cursor()

                cur.execute(
                    """SELECT * FROM (Game INNER JOIN Player
                    ON
                    Game.GAMEID=Player.GAMEID)
                    WHERE Game.GAMEID=?;""", (str(gameID))
                )

                temp = cur.fetchall()
                gameName = temp[1]

                temp = cur.fetchall() # 2D list
                self.player1Name = temp[0][2]
                self.player2Name = temp[1][2]
            else:
                # Constructor 2
                self.gameID = gameID
                self.gameName = gameName
                self.player1Name = player1Name
                self.player2Name = player2Name

                # Maybe turn into helper method setGame
                
                newDB = Database()
                newDB.createDB()
                cur = newDB.conn.cursor()
                cur.execute(
                    """INSERT INTO Game (GAMENAME)
                       VALUES ('""" + str(gameName) + """')
                    """
                )
                newDB.conn.commit()
                gameRowID = cur.lastrowid
                cur.execute(
                    """SELECT * FROM Game WHERE GAMEID = ?""", (gameRowID,))
                temp = cur.fetchone()
                gameID = temp[0]
                self.gameID = gameID

                # print("Gets to inserting players")
                cur.execute(
                    """INSERT INTO Player (GAMEID, PLAYERNAME)
                       VALUES (?, ?)""", (str(gameID), str(player1Name))
                )

                cur.execute(
                    """INSERT INTO Player (GAMEID, PLAYERNAME)
                       VALUES ('""" + str(gameID) + """',
                               '""" + str(player1Name) + """')
                    """
                )

                cur.execute(
                    """INSERT INTO Player (GAMEID, PLAYERNAME)
                       VALUES (?, ?)""", (str(gameID), str(player2Name))
                )
                cur.close()
                newDB.conn.commit()


        except TypeError:
            print("TypeError")
        
    def shoot(self, gameName, playerName, table, xvel, yvel):
        # Use newShot at some point (figure out where/why)

        # print(table)
        
        newDB = Database()
        shotID = newDB.newShot(playerName)

        # get cue ball 
        cueBall = table.cueBall()
        xpos = cueBall.obj.rolling_ball.pos.x
        ypos = cueBall.obj.rolling_ball.pos.y

        rb_speed = math.sqrt(float((xvel * xvel) + (yvel * yvel)))

        xacc = ((-1.0) * (xvel) / rb_speed) * DRAG
        yacc = ((-1.0) * (yvel) / rb_speed) * DRAG

        # Figure out why this is being done in C structure rather than Python classes?
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.number = 0
        cueBall.obj.rolling_ball.pos.x = xpos
        cueBall.obj.rolling_ball.pos.y = ypos
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel
        cueBall.obj.rolling_ball.acc.x = xacc
        cueBall.obj.rolling_ball.acc.y = yacc

        frameCounter = 0
        segmentCounter = 0
        while table is not None:
            oldTime = table.time
            print("\n\nNew iteration", oldTime)
            # print(oldTime)

            # Doing this BEFORE first segment
            oldTable = table
            table = table.segment()
            
            if not table:
                break
            # print(table.time)
            timeDiff = table.time - oldTime
            timeDiff = timeDiff / FRAME_INTERVAL
            timeDiff = math.floor(timeDiff)

            for i in range(0, timeDiff + 1):

                newTable = oldTable.roll(i * FRAME_INTERVAL)

                newTable.time = oldTime + (i * FRAME_INTERVAL)

                frameCounter += 1

                # if newTable.time == 0.0:
                #     copy = Table()
                #     copy.startingTable()
                #     self.write_svg(copy)
                # else:
                # newDB.writeTable(newTable)
                # newDB.update_TableShot(newTable, shotID)
                self.write_svg(newTable)
                extraTable = newTable

            segmentCounter += 1
                
        
        # print(newTable)
        # # newDB.update_TableShot(newTable, shotID)
        # newDB.writeTable(extraTable)
        # extraTable = newDB.readTable(1)
        # print(extraTable)
        # table = newTable
        self.write_svg(newTable)
        return frameCounter - (segmentCounter // 2.3)
            # segmentCounter += 1

    def write_svg(self, table ):
        with open( "table%4.2f.svg" % table.time, "w" ) as fp:
            fp.write( table.svg() )
