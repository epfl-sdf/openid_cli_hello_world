import logging

from .configurer import Configurer
from .messenger import Messenger

logger = logging.getLogger(__name__)


class Client:
    """Client is the main class that carries out the task of talking with the
    oxD server. The oxD commands are provided as class methods that are called
    to send the command to the oxD server via socket.
    """

    def __init__(self, config_location):
        """Constructor of class Client

        Args:
            config_location (string): The complete path of the location
                of the config file. Sample config at
                (https://github.com/GluuFederation/oxd-python/blob/master/sample.cfg)
        """
        self.config = Configurer(config_location)
        self.msgr = Messenger(int(self.config.get("oxd", "port")))
        self.authorization_redirect_uri = self.config.get(
            "client", "authorization_redirect_uri")
        self.oxd_id = None
        if self.config.get("oxd", "id"):
            self.oxd_id = self.config.get("oxd", "id")

            logger.info("Oxd ID found during initialization. Client is"
                        " already registered with the OpenID Provider")
            logger.info("oxd id: %s", self.oxd_id)

        # list of optional params that can be passed to the oxd-server
        self.opt_params = ["op_host",
                           "post_logout_redirect_uri",
                           "client_name",
                           "client_jwks_uri",
                           "client_token_endpoint_auth_method",
                           "client_id",
                           "client_secret",
                           "application_type"]
        self.opt_list_params = ["grant_types",
                                "acr_values",
                                "contacts",
                                "client_logout_uris",
                                "client_request_uris",
                                "client_sector_identifier_uri",
                                "response_types",
                                "scope",
                                "ui_locales",
                                "claims_locales",
                                ]

    def __clear_data(self, response):
        """A private method that verifies that the oxd response is error free
        and raises a RuntimeError when it encounters an error
        """
        if response.status == "error":
            error = "OxD Server Error: {0}\nDescription:{1}".format(
                    response.data.error, response.data.error_description)
            logger.error(error)
            raise RuntimeError(error)
        elif response.status == "ok":
            return response.data

    def register_site(self):
        """Function to register the site and generate a unique ID for the site

        Returns:
            string: The ID of the site (also called client id) if the
            registration is sucessful

        Raises:
            RuntimeError: If the site registration fails.
        """
        if self.oxd_id:
            logger.info('Client is already registered. ID: %s', self.oxd_id)
            return self.oxd_id

        command = {"command": "register_site"}

        # add required params for the command
        params = {
            "authorization_redirect_uri": self.authorization_redirect_uri,
            }
        # add other optional params if they exist in config
        for param in self.opt_params:
            if self.config.get("client", param):
                value = self.config.get("client", param)
                params[param] = value

        for param in self.opt_list_params:
            if self.config.get("client", param):
                value = self.config.get("client", param).split(",")
                params[param] = value

        command["params"] = params
        logger.debug("Sending command `register_site` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

        self.oxd_id = self.__clear_data(response).oxd_id
        self.config.set("oxd", "id", self.oxd_id)
        logger.info("Site registration successful. Oxd ID: %s", self.oxd_id)
        return self.oxd_id

    def get_authorization_url(self, acr_values=None, prompt=None, scope=None):
        """Function to get the authorization url that can be opened in the
        browser for the user to provide authorization and authentication

        Args:
            acr_values (list, optional): acr values in the order of priority
            prompt (string, optional): prompt=login is required if you want to
                force alter current user session (in case user is already
                logged in from site1 and site2 construsts authorization
                request and want to force alter current user session)
            scope (list, optional): scopes required, takes the one provided
                during site registrations by default

        Returns:
            string: The authorization url that the user must access for
            authentication and authorization

        Raises:
            RuntimeError: If the oxD throws an error for any reason.
        """
        command = {"command": "get_authorization_url"}
        if not self.oxd_id:
            self.register_site()

        params = {"oxd_id": self.oxd_id}

        if scope and isinstance(scope, list):
            params["scope"] = scope

        if acr_values and isinstance(acr_values, list):
            params["acr_values"] = acr_values

        if prompt and isinstance(prompt, str):
            params["prompt"] = prompt

        command["params"] = params
        logger.debug("Sending command `get_authorization_url` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

        return self.__clear_data(response).authorization_url

    def get_tokens_by_code(self, code, state):
        """Function to get access code for getting the user details from the
        OP. It is called after the user authorizies by visiting the auth URL.

        Args:
            code (string): code, parse from the callback URL querystring
            state (string): state value parsed from the callback URL

        Returns:
            NamedTuple: The tokens object with the following data structure::

                {
                    "access_token": "<token string>",
                    "expires_in": 3600,
                    "refresh_token": "<token string>",
                    "id_token": "<token string>",
                    "id_token_claims":
                    {
                        "iss": "https://server.example.com",
                        "sub": "24400320",
                        "aud": "s6BhdRkqt3",
                        "nonce": "n-0S6_WzA2Mj",
                        "exp": 1311281970,
                        "iat": 1311280970,
                        "at_hash": "MTIzNDU2Nzg5MDEyMzQ1Ng"
                    }
                }

            Since this would be returned as a NamedTuple, it can be accessed
            using the dot notation as :obj:`data.access_token`,
            :obj:`data.refresh_token`, :obj:`data.id_token`...etc.,

        Raises:
            RuntimeError: If oxD server throws an error OR if the params code
                and scopes are of improper datatype.
        """
        command = {"command": "get_tokens_by_code"}
        params = {"oxd_id": self.oxd_id}
        params["code"] = code
        params["state"] = state

        command["params"] = params
        logger.debug("Sending command `get_tokens_by_code` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        return self.__clear_data(response)

    def get_user_info(self, access_token):
        """Function to get the information about the user using the access code
        obtained from the OP

        Args:
            access_token (string): access token from the get_tokens_by_code
                                    function

        Returns:
            NamedTuple: The user data claims that are returned by the OP.
            Refer to the /.well-known/openid-configuration URL of your OP for
            the complete list of the claims for different scopes.

        Raises:
            RuntimeError: If the param access_token is empty OR if the oxD
                Server returns an error.
        """
        if not access_token:
            logger.error("Empty access code sent for get_user_info")
            raise RuntimeError("Empty access code")

        command = {"command": "get_user_info"}
        params = {"oxd_id": self.oxd_id}
        params["access_token"] = access_token
        command["params"] = params
        logger.debug("Sending command `get_user_info` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

        return self.__clear_data(response).claims

    def get_logout_uri(self, id_token_hint=None, post_logout_redirect_uri=None,
                       state=None, session_state=None):
        """Function to logout the user.

        Args:
            id_token_hint (string, optional): oxd server will use last used
                ID Token, if not provided
            post_logout_redirect_uri (string, optional): URI to redirect,
                this uri would override the value given in the site-config
            state (string, optional): site state
            session_state (string, optional): session state

        Returns:
            string: The URI to which the user must be directed in order to
            perform the logout
        """
        command = {"command": "get_logout_uri"}
        params = {"oxd_id": self.oxd_id}
        if id_token_hint:
            params["id_token_hint"] = id_token_hint

        if post_logout_redirect_uri:
            params["post_logout_redirect_uri"] = post_logout_redirect_uri
        elif self.config.get("client", "logout_redirect_uri"):
            params["post_logout_redirect_uri"] = self.config.get(
                "client", "logout_redirect_uri"
                )

        if state:
            params["state"] = state

        if session_state:
            params["session_state"] = session_state

        command["params"] = params

        logger.debug("Sending command `get_logout_uri` with params %s", params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        return self.__clear_data(response).uri

    def update_site_registration(self):
        """Fucntion to update the site's information with OpenID Provider.
        This should be called after changing the values in the cfg file.

        Returns:
            bool: The status for update. True for success and False for failure
        """
        command = {"command": "update_site_registration"}
        params = {"oxd_id": self.oxd_id,
                  "authorization_redirect_uri": self.authorization_redirect_uri
                  }
        for param in self.opt_params:
            if self.config.get("client", param):
                value = self.config.get("client", param)
                params[param] = value

        for param in self.opt_list_params:
            if self.config.get("client", param):
                value = self.config.get("client", param).split(",")
                params[param] = value

        command["params"] = params
        logger.debug("Sending `update_site_registration` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

        if response.status == "ok":
            return True
        else:
            return False

    def uma_rs_protect(self, resources):
        """Function to be used in a UMA Resource Server to protect resources.

        Args:
            resources (list): list of resource to protect

        Returns:
            bool: The status of the request.
        """
        command = {"command": "uma_rs_protect"}
        params = {"oxd_id": self.oxd_id,
                  "resources": []}

        if len(resources) < 1:
            return False

        params["resources"] = resources
        command["params"] = params

        logger.debug("Sending `uma_rs_protect` with params %s", params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        if response.status == "ok":
            return True
        else:
            return False

    def uma_rs_check_access(self, rpt, path, http_method):
        """Function to be used in a UMA Resource Server to check access.

        Args:
            rpt (string): RPT or blank value if absent (not send by RP)
            path (string): Path of resource (e.g. for http://rs.com/phones,
                /phones should be passed)
            http_method (string) - Http method of RP request (GET, POST, PUT,
                DELETE)

        Returns:
            NamedTuple: The access information recieved in the format below.
            If the access is granted::

                { "access": "granted" }

            If the access is denied with ticket response::

                {
                    "access": "denied",
                    "www-authenticate_header": "UMA realm='example',
                        as_uri='https://as.example.com',
                        error='insufficient_scope',
                        ticket='016f84e8-f9b9-11e0-bd6f-0021cc6004de'",
                    "ticket": "016f84e8-f9b9-11e0-bd6f-0021cc6004de"
                }

            If the access is denied without ticket response::

                { "access": "denied" }

            If the resource is not Protected::

                {
                    "error": "invalid_request",
                    "error_description": "Resource is not protected. Please
                        protect your resource first with uma_rs_protect
                        command."
                }

        """
        command = {"command": "uma_rs_check_access"}
        params = {"oxd_id": self.oxd_id,
                  "rpt": rpt,
                  "path": path,
                  "http_method": http_method}
        command["params"] = params

        logger.debug("Sending command `uma_rs_check_access` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        return self.__clear_data(response)

    def uma_rp_get_rpt(self, force_new=False):
        """Function to be used by a UMA Requesting Party to get RPT token.

        Args:
            force_new (boolean): indicates whether return new RPT, defaults to
                false, so oxd server can cache/reuse same RPT

        Returns:
            String: The RPT token (if recived) or None
        """
        command = {"command": "uma_rp_get_rpt"}
        params = {"oxd_id": self.oxd_id,
                  "force_new": force_new
                  }
        command["params"] = params

        logger.debug("Sending command `uma_rp_get_rpt` with params %s", params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        if response.status == "ok":
            return str(response.data.rpt)
        else:
            return None

    def uma_rp_authorize_rpt(self, rpt, ticket):
        """Function to be used by UMA Requesting Party to authorize a RPT token.

        Args:
            rpt (string): the RPT token to be authorized
            ticket (string): the ticket to authorize the token

        Returns:
            NamedTuple: The server response as an named tuple.
            Authorized Response (Success)::

                { "status":"ok" }

            Not authorized error::

                {
                    "status": "error",
                    "data": {
                        "code": "not_authorized",
                        "description": "RPT is not authorized"
                        }
                }

            Invalid ticket error::

                {
                    "status": "error",
                    "data": {
                        "code": "invalid_ticket",
                        "description": "Ticket is not valid (outdated or not
                            present on Authorization Server)."
                    }
                }

            Invalid rpt error::

                {
                    "status": "error",
                    "data": {
                        "code": "invalid_rpt",
                        "description": "RPT isn't valid (outdated or not
                            present on Authorization Server)."
                    }
                }
        """
        command = {"command": "uma_rp_authorize_rpt"}
        params = {"oxd_id": self.oxd_id,
                  "rpt": rpt,
                  "ticket": ticket
                  }
        command["params"] = params

        logger.debug("Sending command `uma_rp_authorize_rpt` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        return response

    def uma_rp_get_gat(self, scopes):
        """Function to be used by UMA Requesting Party to get a GAT.

        GAT stands for Gluu Access Token. It is invented by Gluu and is
        described here:
        https://ox.gluu.org/doku.php?id=uma:oauth2_access_management

        Args:
            scopes (list): list of strings which describe the scopes

        Returns:
            string: The GAT token. If error, returns None.
        """
        command = {"command": "uma_rp_get_gat"}
        params = {"oxd_id": self.oxd_id,
                  "scopes": scopes
                  }
        command["params"] = params

        logger.debug("Sending command `uma_rp_get_gat` with params %s", params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        if response.status == "ok":
            return str(response.data.rpt)
        else:
            return None
