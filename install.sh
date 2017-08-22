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

#Install a python tool to install python-installer (http://sametmax.com/votre-python-aime-les-pip/)
sudo apt-get install python-setuptools

#Install python-installer for specific version of python and a virtual environnement
sudo easy_install --user pip

#Install virtual environnement for the application to work specifically with python 2.7.12 
#(http://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html)
sudo pip install virtualenv

#Install virtual environnement for the project
#(http://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html)
virtualenv venv

#Install python 2.7.12
sudo apt-get install python2.7.12

#Install required packages
sudo pip install "Flask==0.10.1"
sudo pip install "pyjwkest==1.3.1"

#Make the virtual environnement use python 2.7.12
virtualenv -p /usr/bin/python2.7.12 venv
