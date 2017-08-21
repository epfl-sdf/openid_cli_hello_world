## Usage

```bash
$ python app.py
```
Run the python script, then browse to https://localhost:5443 to see the app.

## settings.json
Settings.json is used as a configuration file for the example app. Change the values to match your system.

Name            | Type    | Mandatory | Default  | Description
----------------| ------- | :-------: | -------- | :---------------
`client_id`     | string  |    ✓      |          | The id for the client. Used to authenticate the client against the authorization server endpoint.
`client_secret` | string  |    ✓      |          | The shared secret to use for authentication against the token endpoint.
`discovery_url` | URL     |           |          | The URL where the metadata of the server can be found. Should contain information about the endpoints and keys to be used. Configuration from the discovery url will override configuration from settings.json.
`scope`         | string  |           | `openid` | The scopes to ask for.
`authorization_endpoint` | URL | if `discovery_url` is not set     |          | The URL to the authorization_endpoint.
`token_endpoint`| URL     |           |          | The URL to the token_endpoint. Mandatory if `discovery_url` is not set.
`issuer`        | string  | if the `openid` scope is requested and `discovery_url` is not set          |          | The ID of the token issuer.
