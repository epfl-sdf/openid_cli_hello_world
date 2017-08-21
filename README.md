## Usage

```bash
$ python app.py
```
Run the python script, then browse to https://localhost:5443 to see the app.

## settings.json
Settings.json is used as a configuration file for the example app.
In order to register the web application in the Gluu server, login in the Gluu server as admin to https://localhost. Manually create a client by selecting in the side bar OpenID Connect > clients, then "add client".

Set the following parameters:

Client Secret: your client id secret of your choosing

Application Type: Native

Pre-Authorization: True

Persist Client Authorizations: False

Subject Type: Pairwise

JWS alg Algorithm for signing the UserInfo Responses: None

JWS alg Algorithm for signing Request Objects: None

Authentication method for the Token Endpoint: None

JWS alg Algorithm for Authentication method to Token Endpoint: None

Redirect Login URIs: https://google.ch

Logout Session Required: False


Leave the other fields empty.
Go at the bottom of the page, click "Add Scope", put openid in the search bar, click search, check the checkbox to add openid as a scope, then ok.
Click "Add Response Type", search "code" and add it.



Name            | Type    | Mandatory | Default  | Description
----------------| ------- | :-------: | -------- | :---------------
`client_id`     | string  |    ✓      |          | The id for the client. Used to authenticate the client against the authorization server endpoint. It may be the Inum name in the description of the client.
`client_secret` | string  |    ✓      |          | The shared secret to use for authentication against the token endpoint.
`redirect_uri`         | string  |           |  | The url you are redirected to after a successful login.
`scope`         | string  |           | `openid` | The scopes to ask for.
`authorization_endpoint` | URL |     |          | The URL to the authorization_endpoint.
`token_endpoint`| URL     |           |          | The URL to the token_endpoint.
`response_type`        | string  |   ✓       |          | Mandatory, hard coded.
