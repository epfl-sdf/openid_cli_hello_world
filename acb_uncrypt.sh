#!/bin/bash
#Décryptage des credentials
#zf170831.1451

ZSECRET="settings.json"

gpg2 $ZSECRET.gpg
#mv $ZSECRET ../.
rm -R ../.gnupg
