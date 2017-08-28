#!/bin/bash
# petit script pour démarrer le Hello Wolrd du client ipenid
#zf170821.1529, 170828.1237

echo "attention ca ne fonctionne pas encore"
exit

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

#adresse IP du serveur
THEIP=$(/sbin/ifconfig ens18 | /bin/grep "inet ad" | /usr/bin/cut -f2 -d: | /usr/bin/awk '{print $1}')

#Tentative d'implementation du screen





#creation de la session screen "proxy"
#screen -S proxy

#creation de la session screen "client"
#screen -S client

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

#echo "Liste des screens actifs"
#screen -list

#echo '------ Créé le screen "client" --------
#Pour creer une fenêtre "client" afin de voir le log du client, faire le raccourci "ctrl-a" puis "c", puis exécuter: "screen -r client"'

#"
#echo '
#------ Créé le screen "proxy" --------
#Pour creer une fenêtre "proxy" afin d'observer les interactions serveur-client, faire le raccourci "ctrl-a" puis "c", puis ex  cuter: "screen -r proxy"

#'
#echo '
#Pour tabber à travers les screens: "CTRL+A", puis "n"
#Plus d'informations sur le fonctionnement de screen: "https://docs.google.com/document/d/1MqJu9ppWayAEUfN6YZkVTt7ERt509_Ake9oafjKemL4/edit"

#'

#lancement du proxy sur la session proxy
#screen -S proxy -X mitmproxy

#creation du dossier virtuel et lancement du programme
#screen -S client -X virtFold="venvOpenid"
#screen -S client -X source $virtFold/bin/activate

#screen -S client -X python app.py

#screen -S client -X deactivate

virtFold="venvOpenid"
source $virtFold/bin/activate

python app.py

deactivate
