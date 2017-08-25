# Creating a client

We want to create a client (web application) which can register a person (EndUser) to the authentication server (our Gluu server).
A user cannot authenticate himself to the Gluu server if he is not registered. Same for the application.

## Registering manually the web application
Go to your server (`https://<your server IP adress>`) and login as the admin (put "admin" in the username field and your password in the password field). You have now arrived on the GUI oxTrust of your Gluu server as the admin. You are ready to manage clients and users of your Gluu server.

We will now register your web application:
Go in the side bar, OpenID Connect>clients, then click on the button "add client" and fill the following fields: Client Name, Client Secret

Go at the bottom of the page, click "add Login Redirect URI", put: `https://<your web application IP adress>:5443/callback`

Go at the bottom of the page, click "add Scope", search for "openid" in the search field, then select "openid", then click the "add" button.

Go at the bottom of the page, click "add Response Type", check the checkbox "code", click "ok".

Click "add" at the very bottom of the page to add your web application. 

Copy the INUM of your client in your clipboard, you will need it later (OpenID Connect>Clients, look for you web application with your Client Name).

## Registering manually the user
Go to the sidebar: Users>add Person

Fill in the fields and remember the username and the password (necessary for basic authentication). Click "add" to add user.

## Configuring your web application (settings.JSON)
Go to your open_client_id folder, (cd open_client...), then open the file "settings.json".

Fill the "client_id" field with your INUM your client display when you view your client under OpenID Connect>Clients (search your client, the INUM is displayed next to it). Paste it if you already had it in your clipboard.

"client_secret" is your client secret.

Leave "response_type" as it is.

To fill the next two fields, you need to go to your Gluu server web interface, search in the side bar for "Configuration>JSON Configuration", select the "OxAuth Configuration" tab.

Look for "authorizationEndpoint", select the displayed url and paste it into the "authorization_endpoint" attribute in your settings.json file.
Then look for "tokenEndpoint", select the displayed url and paste it into the "token_endpoint" attribute.

Set "redirect_uri" to `https://<your web application IP adress>:5443/callback`

You are done configurating your JSON file, save it and exit it.

# Launch your web application
Enter `./start.sh` in your terminal while under openid_cli_hello_world directory.

Open a private navigation window (ctrl-maj-n on chrome, ctrl-maj-p on firefox) so you don't deal with cookies, go to `https:<your web application IP adress>:5443`, click "sign in", log as the user you have added as admin, then ...

## Note
Preferably, you want to launch your web application without cookies related to your web application or Gluu server. Each time you want to use your web application, close all of your browser windows/tabs/..., then open your web application so you won't deal with cookies.
