#!/bin/bash
#Cryptage des credentials
#zf170831.1450

ZSECRET="settings.json"

gpg2 -c ./$ZSECRET
#mv ../$ZSECRET.gpg .
rm -R ../.gnupg
