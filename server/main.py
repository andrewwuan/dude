#!/usr/bin/python


########### TODO #############
# 1. build a port to listen for connection
# 2. no matter what request client sends over, server sends back "hello world"

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb
import MySQLdb
import unicodedata

from audio import *

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="dude database host")
define("mysql_database", default="dude", help="dude database name")
define("mysql_user", default="dude", help="dude database user")
define("mysql_password", default="dude", help="dude database password")

# Map for messages
# In form of:
# dest_user -> [{user: <Original User Name>, message: <Message>}, ...]
messages_map = {}

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/wav", WavHandler),
            (r"/message", MessageHandler),
            (r"/brightness", BrightnessHandler),
            (r"/temperature", TemperatureHandler),
            (r"/last_user", LastUserHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class MainHandler(tornado.web.RequestHandler):
    alarms = ""
    delim = "$"

    def get(self):
        method = self.get_argument("method")
        if (method == "fetch"):
            user = self.get_argument("user")
            name = self.get_argument("name")
            entry = self.application.db.get("SELECT * FROM entries WHERE user = %s AND name = %s",
            user, name)
            self.write(entry.value)
        elif (method == "update"):
            user = self.get_argument("user")
            name = self.get_argument("name")
            value = self.get_argument("value")
            entry = self.application.db.get("SELECT * FROM entries WHERE user = %s", user)
            if not entry:
                self.application.db.execute(
                "INSERT INTO entries VALUES(%s, %s, %s)", user, name, value)
            else:
                self.application.db.execute(
                "UPDATE entries SET name = %s, value = %s"
                "WHERE user = %s", name, value, user)
        elif (method == "update_alarm"):
            request = self.get_argument("request")
            self.alarms = self.alarms + request
            self.alarms = self.alarms + self.delim
        elif (method == "check_alarms"):
            print self.alarms
            self.alarms = self.alarms[0:-1]
            print self.alarms
            self.write(self.alarms)
            self.alarms = ""
            return self.alarms
        else:
            print "Error, method is %s", method


    def post(self):
        f = open("wavfile.wav", "wb")
        f.write(self.request.body)



# Speaker recognition class
class WavHandler(tornado.web.RequestHandler):
    # Do speaker recognition
    def get(self):
        device = self.get_argument('device')
        temp_file = "temp.wav"

        # Write data to a temporary file
        f = open(temp_file, "wb")
        f.write(self.request.body)
        f.close()

        # Do speaker recognition
        users = self.application.db.query("SELECT name,speech_file FROM users")
        print(users)

        if (len(users) == 0):
            self.write('')
        else:
            user = check_audio(temp_file, users)
            # Add last_user to database
            entry = self.application.db.get("SELECT * FROM devices WHERE name=%s", device)
            if entry:
                self.application.db.execute("UPDATE devices SET last_user='%s' WHERE name='%s'" % (user, device))
            else:
                self.application.db.execute("INSERT INTO devices VALUES('%s', '%s', 0, 0)" %
                    (device, user))
            self.write(user)

        os.remove(temp_file)

    # Post new user speech profile
    def post(self):
        user = self.get_argument("user")
        device = self.get_argument('device')
        speech_file = "%s.wav" % user
        self.write("You want to post new speech data to user " + user)

        # Write to file
        f = open(speech_file, "wb")
        f.write(self.request.body)
        f.close()

        # Add user to database
        entry = self.application.db.get("SELECT * FROM users WHERE name=%s", user)
        if not entry:
            self.application.db.execute("INSERT INTO users VALUES(%s, %s)",
                user, speech_file)

        # Add last_user to database
        entry = self.application.db.get("SELECT * FROM devices WHERE name=%s", device)
        if entry:
            self.application.db.execute("UPDATE devices SET last_user='%s' WHERE name='%s'" % (user, device))
        else:
            self.application.db.execute("INSERT INTO devices VALUES('%s', '%s', 0, 0)" %
                (device, user))

# Message class
class MessageHandler(tornado.web.RequestHandler):
    # Get message for user
    def get(self):
        dest_user = self.get_argument("orig_user")
        messages = messages_map.get(dest_user)
        if (messages != None):
            self.write({'messages': messages})
            messages_map[dest_user] = None
        else:
            self.write({'messages': []})

    # Post message to user
    def post(self):
        orig_user = self.get_argument("orig_user")
        dest_user = self.get_argument("dest_user")
        message = self.request.body
        messages = messages_map.get(dest_user)
        if (messages != None):
            messages.append({'user': orig_user, 'message': message})
            messages_map[dest_user] = messages
        else:
            messages_map[dest_user] = [{'user': orig_user, 'message': message}]
        self.write("Message sent")

# Brightness class
class BrightnessHandler(tornado.web.RequestHandler):
    # Get all brightnesses
    def get(self):
        # Get data from MySQL
        data = self.application.db.query("SELECT name,brightness FROM devices")
        print(data)

        self.write({'brightness': data})

    # Post brightness from device
    def post(self):
        device = self.get_argument("device")
        brightness = float(self.request.body)

        # Add brightness to database
        entry = self.application.db.get("SELECT * FROM devices WHERE name=%s", device)
        if entry:
            self.application.db.execute("UPDATE devices SET brightness=%f WHERE name='%s'" % (brightness, device))
        else:
            self.application.db.execute("INSERT INTO devices VALUES('%s', '', 0, %f)" %
                (device, brightness))

# Temperature class
class TemperatureHandler(tornado.web.RequestHandler):
    # Get all temperatures
    def get(self):
        # Get data from MySQL
        data = self.application.db.query("SELECT name,temperature FROM devices")
        print(data)

        self.write({'temperature': data})

    # Post temperature from device
    def post(self):
        device = self.get_argument("device")
        temperature = float(self.request.body)

        # Add temperature to database
        entry = self.application.db.get("SELECT * FROM devices WHERE name=%s", device)
        if entry:
            self.application.db.execute("UPDATE devices SET temperature=%f WHERE name='%s'" % (temperature, device))
        else:
            self.application.db.execute("INSERT INTO devices VALUES('%s', '', %f, 0)" %
                (device, temperature))

        self.write("Temperature set")

# Brightness class
class LastUserHandler(tornado.web.RequestHandler):
    # Get all last users
    def get(self):
        # Get data from MySQL
        data = self.application.db.query("SELECT name,last_user FROM devices")
        print(data)

        self.write({'last_user': data})

prompt = """Usage:
GET /wav:   
    request:
        body: wav file
    response:
        voice recognized user name
POST /wav:
    request:
        parameters: user
        body: wav file
    response:
        acknowledgement
GET /message:
    request:
        parameters: orig_user
    response:
        A list of messages for orig_user in {user:<Name>, message:<Message>} format, 
            or "No new messages" if there're no messages.
POST /message:
    request:
        parameters: orig_user, dest_user
        body: message
    response:
        "Message send"

GET /brightness:
    response:
        A list of brightnesses for all devices

POST /brightness:
    request:
        parameters: device
        body: brightness
    response
        "Brightness set"

GET /temperature:
    response:
        A list of temperatures for all devices

POST /temperature:
    request:
        parameters: device
        body: temperature
    response
        "Temperature set"

GET /last_user:
    response:
        A list of last_user for all devices

Using curl:
(Replace arguments enclosed by <>)
Run voice recognition:
    curl -X GET http://<hostname>:8888/wav --data-binary @<audio>.wav
Post new user voice data:
    curl -X POST http://<hostname>:8888/wav?user=<name> --data-binary @<audio>.wav
Check message:
    curl -X GET http://<hostname>:8888/message?orig_user=<name>
Send message:
    curl -X POST http://<hostname>:8888/message?orig_user=<name>&dest_user=<name> --data <message>
"""

def main():
    print prompt
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
