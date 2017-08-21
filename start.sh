#!/bin/bash
# petit script pour démarrer le Hello Wolrd du client ipenid
#zf170821.1529

#source: 

THEIP=$(/sbin/ifconfig ens18 | /bin/grep "inet ad" | /usr/bin/cut -f2 -d: | /usr/bin/awk '{print $1}')


#virtFold="venvURL"

# Teste si les arguments sont bien passés 
#if (( $# < 2 ))
#then
#    echo "Erreur: pas assez d'arguments
#    usage: ./start.sh fichier_du_script quantité_de_RAM_maximale"
#    exit
#fi

# Teste si fichier existe
#if [ -e "$1" ]
#then
#    CMD=$(sed -n 2p $1)
#    CMD_NAME=$(echo $CMD | awk '{print $1}')
#    echo "Name: "$CMD_NAME
#else
#    echo Pas de fichier $1 
#    exit
#fi

echo -e " 
Afin de garder le proxy WEB permanent, il serait bien de le faire tourner dans un 'screen' avec:
screen -S testwwp     pour entrer dans screen
./web_server.sh       pour lancer le serveur WEB dans screen
CTRL+a,d              pour sortir de screen en laissant tourner le serveur
screen -r testwwp     pour revenir dans screen
CTRL+d                pour terminer screen
screen -list          pour lister tous les screen en fonctionement

On accède à ce petit Hello Word avec:

https://$THEIP:5443


"

# lance le virtualenv
#source $virtFold/bin/activate 

python app.py

