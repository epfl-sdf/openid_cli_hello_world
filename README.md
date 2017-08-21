# openid_cli_hello_world
Petit Hello World pour tester en tant que client un serveur OpenID

Fully based on https://github.com/curityio/example-python-openid-connect-client

1. clone the repository https://github.com/curityio/example-python-openid-connect-client

2.. Register the client in your OpenID server:

(Gluu server example)
3. fill out the following:
  Client Name: (eg. python-client-example)
  Application Type: Web
  Pre-Authorization: True
  Subject Type: public
  Response Types: code
  
  add Scope: user_name
  add login redirect uri: (your client's redirect uri, eg. https://\<localhost\>:5443/callback
  
4. Update your settings.json file with your client_id and the rest to match your own server

