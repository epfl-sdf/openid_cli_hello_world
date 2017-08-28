#!/bin/bash
# petit script pour installer le Hello Wolrd du client openid
#zf170821.1715

#source: https://github.com/curityio/example-python-openid-connect-client



#virtFold="venvURL"
#sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev
#sudo apt install virtualenv
#rm -rf $virtFold
#virtualenv -p /usr/bin/python3 venvURL
#source $virtFold/bin/activate 
#pip3 install mitmproxy
#pip3 install beautifulsoup4
#deactivate

echo ------------ install mitmproxy
sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev
pip3 install mitmproxy

echo ------------ install virtualenv
sudo apt-get -y install python-pip
sudo pip2 install virtualenv

#Create virtual environement folder
virtFold="venvOpenid"
rm -rf $virtFold
virtualenv -p /usr/bin/python2 $virtFold
source $virtFold/bin/activate

#Install required packages
pip2 install -r requirements.txt

deactivate
