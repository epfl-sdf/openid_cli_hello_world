"""
A simple CLI script to test native app implementation of OIDC using oxd-python
"""
import os
import sys
import logging

import requests

this_dir = os.path.dirname(os.path.realpath(__file__))
config = os.path.join(this_dir, 'native.cfg')

oxd_path = os.path.dirname(this_dir)
if oxd_path not in sys.path:
    sys.path.insert(0, oxd_path)

import oxdpython

client = oxdpython.Client(config)
logging.basicConfig(level=logging.DEBUG)


def get_auth_url():
    logging.debug('Fetching authorization url.')
    auth_url = client.get_authorization_url(['oath'])
    logging.debug('Calling the auth_url: %s', auth_url)
    return auth_url


def register():
    logging.debug('Registering native app')
    oxid = client.register_site()
    logging.debug('Registration successful. ID: %s', oxid)


def run():
    logging.debug('Starting nativeapp')
    register()
    auth_url = get_auth_url()
    r = requests.get(auth_url, verify=False)
    print "Status Code: ", r.status_code
    print "Headers: ", r.headers
    print "URL: ", r.url

    token = 123456
    r2 = requests.post(r.url, data={"username": "admin", "token": token},
                       verify=False)
    print "Status Code: ", r2.status_code
    print "Text: ", r2.text
    print "Headers: ", r2.headers
    print "URL: ", r2.url


if __name__ == '__main__':
    run()
