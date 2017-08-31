# Table des matières
1. [Créer un client](#creer_client)
    1. [Accès à l'interface d'administration du serveur](#GUI)
    2. [Enregistrer le client:](#enr_client)
    3. [Enregistrer manuellement l'utilisateur](#enr_user)
2. [Configuration du client](#conf_client)
3. [(Dé)cryptage du fichier settings.json](#client_crypt)
3. [Lancer le client (et le proxy)](#client_launch)
4. [Note](#notes)


## Créer un client<a name="creer_client"></a>
Petit client (application web) pouvant authentifier un utilisateur (EndUser) à un serveur d'authentification OpenID (par exemple votre serveur Gluu).<br>
Un utilisateur ne peut pas se connecter au serveur d'identification si celui-ci n'est pas enregistré sur le serveur, de même pour l'application web.

### Accès à l'interface d'administration du serveur<a name="GUI"></a>
Allez sur votre serveur (https://\<IP de votre serveur\>, n'oubliez pas le https:// !) avec votre navigateur (de préférence chrome ou firefox) et connectez-vous en tant qu'administrateur (mettez "admin" comme nom d'utilisateur et votre mot de passe (du serveur Gluu)).
Vous arrivez sur l'interface OxTrust vous permettant d'administrer les utilisateurs et les clients.

### Enregistrer le client<a name="enr_client"></a>
Allez dans la barre latérale, `OpenID Connect>clients`, puis cliquez sur *add client* et remplissez les champs: *Client Name*, *Client Secret*

Notez le *Client Secret*, nous en aurons besoin plus tard.

Allez en bas de la page, cliquez sur *add Login Redirect URI*, mettez: https://\<IP de votre application web\>:5443/callback

Allez en bas de la page, cliquez sur *add Scope*, cherchez *openid* dans la barre de recherche, sélectionnez *openid*, puis cliquez sur  le bouton *add*.

Allez en bas de la page, cliquez sur *add Response Type*, validez *code*, cliquez sur *ok*.

Cliquez *add* tout en bas de la page pour ajouter votre client. 

Copier l'*INUM* de votre client dans le presse-papier, vous en aurez besoin plus tard.<br>
Si vous en aviez besoin plus tard, on peut le retrouver dans `OpenID Connect>Clients` , cherchez votre client avec le Client Name correspondant

### Enregistrer manuellement l'utilisateur<a name="enr_user"></a>
Toujours dans l'interface d'administration, allez dans la barre latérale: `Users>add Person`

Remplissez les champs et notez le username ainsi que le password (pour l'authentification). Cliquez sur *add* pour ajouter l'utilisateur.

Ne fermez pas encore l'interface, vous en aurez encore besoin.

## Configuration du client (settings.JSON)<a name="conf_client"></a>
Naviguez dans votre dossier *openid_cli_hello_world*, (`cd openid_cli_hello_world`), copiez settings.json.template en settings.json, puis ouvrez le fichier *settings.json* afin de le configurer.

Remplissez "client_id" par votre INUM (pour rappel, il est visible sous OpenID Connect>Clients) ou collez-y ce que vous aviez dans le presse-papier.

Remplissez "client_secret" par votre *Client Secret*.

Sélectionnez pour "Authentication method for the Token Endpoint" la méthode *client_secret_post*

Mettez dans "redirect_uri" l'url que vous trouverez au même endroit que le *client_id*

Puis remplissez les champs:

 "response_type": "code",
 "verify_ssl_server": "false",
 "scope": "openid",
  
Pour remplir les prochains champs, vous aurez besoin de retourner sur l'interface d'administration du serveur Gluu, dans la barre latérale `Configuration>JSON Configuration` et sélectionner l'onglet *OxAuth Configuration*.

Cherchez chaque fois les bonnes URL's pour les champs suivants:

"authorization_endpoint": cherchez *authorizationEndpoint*
"token_endpoint": cherchez *tokenEndpoint*
"issuer": cherchez *Issuer*
"jwks_uri": cherchez *jwksUri*

Vous avez terminé de configurer votre fichier settings.json, sauvez-le et revenez dans le dossier openid_cli_hello_world.

## (Dé)cryptage du fichier settings.json <a name="client_crypt"></a>
Vous pouvez (dé)crypter le fichier "settings.json" en exécutant: `./acb_crypt.sh` (`./acb_uncrypt.sh`) avec un mot de passe de votre choix.

## Lancer le client (et le proxy) <a name="client_launch"></a>
Vérifiez que vous avez un fichier "settings.json" non-crypté.

On rappelle que screen est un outil très utile pour faire tourner une application:
Afin de garder l'appli permanente, il serait bien de la faire tourner dans un 'screen' avec:

screen -S *openid*    pour entrer dans screen<br>
./start.sh            pour lancer le client une fois dans le screen openid<br>
CTRL+a,d              pour sortir de screen en laissant tourner le serveur<br>
screen -r *openid*      pour revenir dans le screen openid<br>
CTRL+d                pour terminer screen<br>
screen -list          pour lister tous les screen en fonctionement<br>

Executez `./start.sh` pour lancer le client.

Si vous désirez voir le client à l'aide d'un proxy, lancer le proxy (dans un screen *proxy* par exemple) avec `./mitmproxy/start_mitmproxy.sh` 

Ouvrez une fenêtre de navigation privée (ctrl-maj-n sur chrome, ctrl-maj-p sur firefox) afin de ne pas avoir affaire à d'anciens cookies. Allez sur https:\<adresse IP de votre client\>:5443, cliquez sur *sign in* puis connectez-vous en tant qu'utilisateur.

## Note<a name="notes"></a>
__Faites attention à chaque tentative de connexion__: fermez toutes vos fenêtre actives de votre navigateur puis ouvrez une fenêtre de navigation **privée** afin de ne pas avoir affaire aux cookies perturbant l'authentification.