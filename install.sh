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

echo ------------ apt-get install python3
sudo apt-get install -y python3 python3-pip

echo ------------ install virtualenv
sudo pip2 install virtualenv
#Create virtual environement folder
sudo virtualenv ./.venv

#Install python 2.7.12
sudo apt-get install python2.7.12

#Install required packages
pip install Flask-SSLify
sudo apt install Flask-SSLify-pip
sudo pip install pycryptodomex

#Make the virtual environnement use python 2.7.12
sudo virtualenv -p /usr/bin/python2.7 venv
