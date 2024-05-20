import sys
import cgi
import phylib
import Physics
import os
import re
import math
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import urlparse, parse_qsl

pattern = re.compile(r'^(\/table-\d+\.svg)$')
MAX_SPEED = 4000.0 # mm/s

class MyHandler(BaseHTTPRequestHandler):
    game = None
    table = None
    frameCount = 0

    def do_GET(self):
        parsed = urlparse(self.path)

        #Check for poolgame.html
        if (parsed.path in ['/poolgame.html']):

            #retrieve HTML file

            value = self.path
            str_list = ['/poolgame.html?xvel=', 'yvel=', 'nothing']
            for string in str_list:
                value = value.replace(string, '')

            str_list = value.split(',')

            print(str_list)
            newDB = Physics.Database()

            # print(str_list)
            if len(str_list) == 2:
                x_vel = float(str_list[0])
                y_vel = float(str_list[1])
                # tableID = int(str_list[2])

                # print(x_vel, y_vel)
                if not self.game:
                    self.game = Physics.Game(gameName='Game 1', player1Name='bitch', player2Name='cunt')  

                    
                
                # fp = open("reference.svg")
                # stuff = fp.read()
                if os.path.exists("reference.svg"):
                    self.table = Physics.Table()
                    self.table.readSvg("reference.svg")
                    fp = open("frameCount.txt", "r")
                    self.table.time = float(fp.read()) / 100.0
                    # self.table.time = 0.0
                    print(self.table)
                else:
                    self.table = Physics.Table()
                    self.table.startingTable()
                
                x_vel = (-5.0) * x_vel
                y_vel = (-5.0) * y_vel

                if math.fabs(x_vel) > MAX_SPEED:
                    if x_vel > 0:
                        x_vel = MAX_SPEED
                    else:
                        x_vel = (-1.0) * MAX_SPEED
                if math.fabs(y_vel) > MAX_SPEED:
                    if y_vel > 0:
                        y_vel = MAX_SPEED
                    else:
                        y_vel = (-1.0) * MAX_SPEED

                self.frameCount = self.game.shoot("Game 1", "bitch", self.table, x_vel, y_vel)
                # print(self.table)
                # newDB.writeTable(self.table)

                # print(newDB.readTable(1))
                # holy fuck maybe i can send it to the response of this
                # see if that makes sense (response to fetch that sends velocities to server)
                print(self.frameCount)


                if os.path.exists("frameCount.txt"):
                    fp = open("frameCount.txt", "r")
                    newNum = fp.read()
                    self.frameCount += int(float(newNum))
                    print(self.frameCount)
                    os.remove("frameCount.txt")
                fp = open("frameCount.txt", "w")
                fp.write(str(self.frameCount))

                str_list = ['1', '2', '3']

                fp = open('.'+parsed.path)
                content = fp.read()

                #generate headers
                self.send_response(200) #OK
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(content))
                self.end_headers()

                self.wfile.write(bytes(content, "utf-8"))

                fp.close()

                # return self.frameCount
                # check what this does and adpt to work
                # can also use another function for frameCount instead of shoving it into this (look)

            else:
                # print("Entered else")
                self.game = Physics.Game(gameName='Game 1', player1Name='bitch', player2Name='cunt')
                # print(self.game)
                self.table = Physics.Table()
                self.table.startingTable()

            fp = open('.'+parsed.path)
            content = fp.read()

            #generate headers
            self.send_response(200) #OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))

            fp.close()

        elif (parsed.path.__contains__(".svg")): #filename being checked using regex (see 'pattern' variable above)

            #retrieve svg file
            # print(parsed.path)
            filename = parsed.path
            print(filename)
            str_list = filename.split("/")
            # print(str_list)

            self.frameCount = int(float(str_list[1]))

            # filename = filename.replace("/", "")
            # number = filename.replace("table", "")
            # number = number.replace(".svg", "")
            # number = float(number)

            if os.path.exists(str_list[2]): # accounting for svg not existing
                # print(str_list[2])
                fp = open(str_list[2])
                content = fp.read()
                if os.path.exists("reference.svg"):
                    # print("reference exists, overwrite")
                    os.remove("reference.svg")
                # print("writing reference", content)
                fp = open("reference.svg", "w")
                fp.write(content)
            else:
                # increment counter for table svg
                # copy frame in case of missing image
                filename = parsed.path
                filename = str_list[2].replace("table", "")
                filename = filename.replace(".svg", "")

                # print(filename)

                if float(filename) * 100.0 >= self.frameCount:
                    filename = float(self.frameCount / 100.0)
                    # print("numero uno", self.frameCount, filename)
                elif float(filename) > 0.0:
                    filename = float(filename)# display next file again (will result in laggy animation)
                    # print("numero dos", filename)
                else:
                    filename = float(filename)
                    # print("numero three", filename)
                number = filename
                filename = "table%.2f.svg" % filename

                
                # fp = open("reference.svg")
                print(self.table)

                # print(filename)
                # if os.path.exists(filename) and number <= (self.frameCount / 100.0) - 0.03:
                #     print("numba 1", number)
                #     self.table = Physics.Table()
                #     self.table.readSvg(filename)
                #     fp = open(filename)
                # else:
                number = float(self.frameCount / 100.0)
                print("numba 2", number)
                self.table = Physics.Table()
                self.table.readSvg("table%.2f.svg" % number)
                fp = open("table%.2f.svg" % number)
                content = fp.read()
                
                if os.path.exists("reference.svg"):
                    # print("reference exists, overwrite")
                    os.remove("reference.svg")
                # print("writing reference", content)
                fp = open("reference.svg", "w")
                fp.write(content)

            #generate headers
            # print(nu)
            time.sleep(0.01)    
            
            self.send_response(200) # OK
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(content))
            self.end_headers()

            #send to browser
            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
        # Add condition to get for getting frameCount
        # Figure out some kind of condition i can add (in JS?) for when the frameCount is needed
        # Condition needs to be passed into server somehow, try through url like before
        # if (condition) then send content (variable) to JS and recieve in the response to fetch()
            
        elif 'getFrameCount' in parsed.path:
            # print("entered frame")

            fp = open("frameCount.txt", "r")
            self.frameCount = fp.read()

            # print(self.frameCount)

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/plain")  # Return as plain text
            self.send_header("Content-length", len(str(self.frameCount)))
            self.end_headers()
            # print(self.frameCount)
            # print(str(self.frameCount))
            self.wfile.write(str(self.frameCount).encode("utf-8"))
            return  # Exit the function
        
        elif 'replaceBall' in parsed.path:
            table = Physics.Table()
            table.readSvg("reference.svg")
            table += Physics.StillBall(0, Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0))
            os.remove("reference.svg")
            fp = open("reference.svg", "w")
            fp.write(table.svg())

            self.send_response(200)  # OK
            self.end_headers()
            return
        
        elif parsed.path in ['/names.html']:
            fp = open('.'+self.path)
            content = fp.read()

            #generate headers
            self.send_response(200) # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # send to browser
            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
        
        elif 'getName1' in parsed.path:
            fp = open('p1name.txt', 'r')
            name = fp.read()
            print(name)

            self.send_response(200) # OK
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(str(name)))
            self.end_headers()

            self.wfile.write(str(name).encode("utf-8"))
            return
        
        elif 'getName2' in parsed.path:
            fp = open('p2name.txt', 'r')
            name = fp.read()
            print(name)

            self.send_response(200) # OK
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(str(name)))
            self.end_headers()

            self.wfile.write(str(name).encode("utf-8"))
            return

        # elif 'getFrames' in parsed.path:
        #     # send all svgs as array of strings
        #     svgList = []
        #     for i in range(self.frameCount):
        #         fp = open("table%.2f.svg" % (self.frameCount / 100.0), "r")
        #         svgList.append(fp.read())
        #     self.send_response(200) # OK
        #     self.send_header("Content-type", "text/plain")
        #     self.send_header("Content-length", len(svgList))
        #     self.end_headers()
        #     self.wfile.write(svgList.encode("utf-8"))
        #     return
            
        # elif 'getFrames' in parsed.path:
            
        #     filename = parsed.path
        #     filename = filename.replace("/table", "")
        #     filename = filename.replace(".svg", "")
        #     time.sleep(0.01 * float(filename))


        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)

        #create new file display.html
        if (parsed.path in ['/poolgame.html']):

            form = cgi.FieldStorage(
                fp = self.rfile,
                headers=self.headers,
                environ = {
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE':
                    self.headers['Content-Type']
                }
            )

            p1name = form.getvalue('p1_input')
            p2name = form.getvalue('p2_input')


            if p1name and p2name:
                fp = open('p1name.txt', "w")
                fp.write(p1name)
                fp = open('p2name.txt', 'w')
                fp.write(p2name)
            else:
                fp = open('p1name.txt', "w")
                fp.write('Charles Leclerc')
                fp = open('p2name.txt', 'w')
                fp.write('A fucking wall')

            fp = open('.'+self.path)
            content = fp.read()

            #generate the headers
            self.send_response(200) # OK
            self.send_header("Content-type", "text/html")

            #send it to browser
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
            fp.close()

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
    print("Server listing in port:  ", int(sys.argv[1]))
    httpd.serve_forever()
