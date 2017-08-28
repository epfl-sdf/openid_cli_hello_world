#!/bin/bash
# petit script pour démarrer le Hello Wolrd du client ipenid
#zf170821.1529

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


#creation de la session screen "proxy"
screen -S proxy

#creation de la session screen "client"
screen -S client

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

echo "Liste des screens actifs"
screen -list

echo '------ Créé le screen "client" --------
Pour switcher au screen "client" afin le log de l'application client, exécuter: "screen -r client"'

"
echo '
------ Créé le screen "proxy" --------
Pour switcher au screen "proxy" afin d'observer les échanges serveur-client, exécuter: "screen -r proxy"

'
echo '
Pour tabber à travers les screens: "CTRL+A", puis "n"
Plus d'informations sur le fonctionnement de screen: "https://docs.google.com/document/d/1MqJu9ppWayAEUfN6YZkVTt7ERt509_Ake9oafjKemL4/edit"

'

#creation du dossier virtuel et lancement du programme
virtFold="venvOpenid"
source $virtFold/bin/activate

python app.py

deactivate

