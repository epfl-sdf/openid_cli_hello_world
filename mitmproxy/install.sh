#!/bin/bash
# petit script pour installer le proxy mitmproxy
#zf170901.1446

#source: 

echo ------------ start

echo ------------ apt-get install utils
sudo apt-get update
sudo apt-get -y install python3-dev python3-pip libffi-dev libssl-dev
export LC_ALL=C

echo ------------ install virtualenv
#sudo apt-get -y install python-pip
export LC_ALL=C
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv


echo ------------ install mitmproxy
virtFold="venvMitmproxy"
rm -rf $virtFold
virtualenv -p /usr/bin/python3 $virtFold
source $virtFold/bin/activate
sudo -H pip3 install mitmproxy

deactivate

