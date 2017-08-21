## Usage

```bash
$ python app.py
```
Run the python script, then browse to https://localhost:5443 to see the app.

## settings.json
Settings.json is used as a configuration file for the example app. Change the values to match your system.

Name            | Type    | Mandatory | Default  | Description
----------------| ------- | :-------: | -------- | :---------------
`client_id`     | string  |    ✓      |          | The id for the client. Used to authenticate the client against the authorization server endpoint. It may be the Inum name in the description of the client.
`client_secret` | string  |    ✓      |          | The shared secret to use for authentication against the token endpoint.
`redirect_uri`         | string  |           |  | The url you are redirected to after a successful login.
`scope`         | string  |           | `openid` | The scopes to ask for.
`authorization_endpoint` | URL |     |          | The URL to the authorization_endpoint.
`token_endpoint`| URL     |           |          | The URL to the token_endpoint.
`response_type`        | string  |          |          | Mandatory, hard coded.
