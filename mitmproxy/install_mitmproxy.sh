#!/bin/bash
#Create virtual environement folder
virtFold="venvMitmproxy"
rm -rf $virtFold
virtualenv -p /usr/bin/python3 $virtFold
source $virtFold/bin/activate
sudo pip3 install mitmproxy

deactivate

