#!/usr/bin/python

import Cookie
import os
import shelve
import time
import traceback

from constants import *
from appLog import *

html = """<HTML><HEAD><TITLE>%(title)s</TITLE></HEAD>
<BODY>
<H1>%(title)s</H1>
%(message)s
<hr>
</BODY>
</HTML>
"""

message = """<P><a href="%s">OpenID Connect Login</a></P>""" % GET_AUTH_URL
envs = os.environ
sub = None
if 'HTTP_COOKIE' in envs:
    cookie_string=envs['HTTP_COOKIE']
    c=Cookie.SimpleCookie()
    c.load(cookie_string)
    try:
        session_id = c['session'].value
        db = shelve.open(DB_FILENAME)
        sub = db[session_id]['sub']
        exp = int(db[session_id]['exp'])
        db.close()
        os.environ['TZ'] = TZ
        time.tzset()
        expiration_time =  time.strftime('%x %X %Z', time.localtime(exp))
        message = """Subject: %s
Application Session Expires: %s
<P><a href="%s">OpenID Connect Logout</a> </P>""" % (sub, expiration_time, GET_LOGOUT_URL)
    except KeyError:
        message = "No session found. <BR>" + message
        logException("Error returning home page...")


if sub:
    log("Printing homepage for sub %s" % sub)
else:
    log("Printing homepage with link to login.")

d = {}
d['title'] = TITLE
d['message'] = message

print "Content-type: text/html"
print
print html % d 

