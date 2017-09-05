#!/bin/bash
# lancement du proxy a partir de l'environnement virtuel
#zf170901.1530

virtFold="venvMitmproxy"
source $virtFold/bin/activate

# pour les problèmes de SNI il faut lire
# http://docs.mitmproxy.org/en/stable/features/passthrough.html
 
#mitmdump -v
mitmdump --insecure
#mitmproxy


deactivate
