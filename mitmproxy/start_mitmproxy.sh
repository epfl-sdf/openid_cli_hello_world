#!/bin/bash
# lancement du proxy a partir de l'environnement virtuel
virtFold="venvMitmproxy"
source $virtFold/bin/activate

mitmproxy

deactivate
