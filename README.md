# Petit Hello World pour tester en tant que client un serveur OpenID

Petit client (application web) pouvant authentifier un utilisateur (EndUser) à un serveur d'authentification OpenID (par exemple votre serveur Gluu). 

## Installation de l'application web (client)
Lancer le fichier d'installation
```
./install.sh
```

## Configuration et lancement du client
Puis lire la documentation:<br>
https://github.com/epfl-sdf/openid_cli_hello_world/blob/master/DOC.md

## Proxy mitmproxy

### Pour lancer le proxy
qui permet de 'voir' la communication il faut faire:
```
./mitmproxy/install.sh
```

### Pour démarrer le proxy
il faut faire:
```
./mitmproxy/start.sh
```

ATTENTION: il y a un problème avec le SNI, il faut lire l'url qui se trouve dans le ./mitmproxy/start.sh !



## Sources:
La majorité du code provient de l'example https://github.com/curityio/example-python-openid-connect-client créé par https://curity.io
