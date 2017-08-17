#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
location = '/var/www/html/oxd-python/demosite/'
if not location in sys.path:
    sys.path.insert(0, location)

import demosite
application = demosite.app
