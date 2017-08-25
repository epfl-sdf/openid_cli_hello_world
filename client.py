##########################################################################
# Copyright 2016 Curity AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import json
import ssl
import urllib
import urllib2

import tools


class Client:
    def __init__(self, config):
        self.ctx = ssl.create_default_context()
        self.config = config
        self.__init_config()

    def __init_config(self):
        if 'verify_ssl_server' in self.config and not self.config['verify_ssl_server']:
            self.ctx.check_hostname = False
            self.ctx.verify_mode = ssl.CERT_NONE

        if 'discovery_url' in self.config:
            discovery = urllib2.urlopen(self.config['discovery_url'], context=self.ctx)
            self.config.update(json.loads(discovery.read()))
        else:
            print "No discovery url configured, all endpoints needs to be configured manually"

        # Mandatory settings
        if 'authorization_endpoint' not in self.config:
            raise Exception('authorization_endpoint not set.')
        if 'token_endpoint' not in self.config:
            raise Exception('token_endpoint not set.')
        if 'client_id' not in self.config:
            raise Exception('client_id not set.')
        if 'client_secret' not in self.config:
            raise Exception('client_secret not set.')
        if 'redirect_uri' not in self.config:
            raise Exception('redirect_uri not set.')

        if 'scope' not in self.config:
            self.config['scope'] = 'openid'

    def revoke(self, token):
        """
        Revoke the token
        :param token: the token to revoke
        :raises: raises error when http call fails
        """
        if 'revocation_endpoint' not in self.config:
            print 'No revocation endpoint set'
            return

        revoke_request = urllib2.Request(self.config['revocation_endpoint'])
        data = {
                'token': token,
            	'client_id': self.config['client_id'],
            	'client_secret': self.config['client_secret']
        }
        urllib2.urlopen(revoke_request, urllib.urlencode(data), context=self.ctx)

    def refresh(self, refresh_token):
        """
        Refresh the access token with the refresh_token
        :param refresh_token:
        :return: the new access token
        """
        data = {
		'grant_type': 'refresh_token',
            	'refresh_token': refresh_token,
            	'client_id': self.config['client_id'],
            	'client_secret': self.config['client_secret']
        }
        token_response = urllib2.urlopen(self.config['token_endpoint'], urllib.urlencode(data), context=self.ctx)
        return json.loads(token_response.read())

    def get_authn_req_url(self, session):
        """
        :param session: the session, will be used to keep the OAuth state
        :return redirect url for the OAuth code flow
        """
        state = tools.generate_random_string()
        session['state'] = state
        request_args = self.__authn_req_args(state)
        login_url = "%s?%s" % (self.config['authorization_endpoint'], urllib.urlencode(request_args))
        print "Authorization %s" % login_url
        return login_url

    def get_token(self, code):
        """
        :param code: The authorization code to use when getting tokens
        :return the json response containing the tokens
        """
        # Assignment 1
        # Fill in the the missing data for the token request
        data = {
		'scope': self.config['scope'],
		'response_type': 'code',
		'client_id': self.config['client_id'],
		'redirect_uri': self.config['redirect_uri']
		}
	#https://gluu.org/docs/ce/api-guide/openid-connect-api/ (required fields from Gluu server)

        # Exchange code for tokens
	print "trying to get the token from "
	print self.config['token_endpoint']
	print "\n with the following data"
	print data
	print "\n\n encoded data"
	print urllib.urlencode(data)
	print "\n\n"
        token_response = urllib2.urlopen(self.config['token_endpoint'], urllib.urlencode(data), context=self.ctx)
        print "token response:"
	print token_response
	return json.loads(token_response.read())

    def __authn_req_args(self, state):
        """
        :param state: state to send to authorization server
        :return a map of arguments to be sent to the authz endpoint
        """
        args = {
		'scope': self.config['scope'],
                'response_type': 'code',
                'client_id': self.config['client_id'],
                'state': state
	}

        if 'authn_parameters' in self.config:
            args.update(self.config['authn_parameters'])
        return args
