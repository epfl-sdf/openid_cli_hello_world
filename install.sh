#!/bin/bash
# petit script pour installer le Hello Wolrd du client openid
#zf170831.1441

#source: https://github.com/curityio/example-python-openid-connect-client

echo ------------ start

echo ------------ apt-get install utils
sudo apt-get update
sudo apt-get install -y gnupg2 jq

echo ------------ secrets uncrypt
./acb_uncrypt.sh

#echo ------------ install mitmproxy
#sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev
#pip3 install mitmproxy

echo ------------ install virtualenv
sudo apt-get -y install python-pip
export LC_ALL=C
sudo -H pip2 install --upgrade pip
sudo -H pip2 install virtualenv

echo ------------ create virtualenv
#Create virtual environement folder
virtFold="venvOpenid"
rm -rf $virtFold
virtualenv -p /usr/bin/python2 $virtFold
source $virtFold/bin/activate

echo ------------ install required package
#Install required packages
pip2 install -r requirements.txt

deactivate
echo ------------ end
