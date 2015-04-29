#!/usr/bin/python

import string

def check_message(user):
        # Check server and fetch message for user

        user2 = ""
        message = ""
        return [user2, message]  

def send_message(message, user, user2):
        # Convert I to user name
        message = message.replace("i ", "%s " % (user))
        message = message.replace("I ", "%s " % (user))
        # Send the message to server (user -> user2)

        return
