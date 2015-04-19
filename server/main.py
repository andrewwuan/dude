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

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/wav", WavHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument("user")
        name = self.get_argument("name")
        value = self.get_argument("value", None)
        if (not value):
            entry = self.application.db.get("SELECT * FROM entries WHERE user = %s AND name = %s",
                user, name)
            self.write(entry.value)
        else:
            entry = self.application.db.get("SELECT * FROM entries WHERE user = %s", user)
            if not entry:
                self.application.db.execute(
                "INSERT INTO entries VALUES(%s, %s, %s)", user, name, value)
            else:
                self.application.db.execute(
                "UPDATE entries SET name = %s, value = %s"
                "WHERE user = %s", name, value, user) 

    def post(self):
        f = open("wavfile.wav", "wb")
        f.write(self.request.body)



# Speaker recognition class
class WavHandler(tornado.web.RequestHandler):
    # Do speaker recognition
    def get(self):
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
            self.write(check_audio(temp_file, users))

        os.remove(temp_file)

    # Post new user speech profile
    def post(self):
        user = self.get_argument("user")
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


prompt = """Usage:
GET /wav:   
    request:
        parameters: (none)
        body: wav file
    response:
        voice recognized user name
POST /wav:
    request:
        parameters: user
        body: wav file
    response:
        acknowledgement

Using curl:
(Replace arguments enclosed by <>)
Run voice recognition:
    curl -X GET http://<hostname>:8888/wav --data-binary @<audio>.wav
Post new user voice data:
    curl -X POST http://<hostname>:8888/wav?user=<name> --data-binary @<audio>.wav
"""

def main():
    print prompt
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
