# Integration script that will enable OATH PIN based authentication
# in oxAuth using the python-oath
from org.xdi.model.custom.script.type.auth import PersonAuthenticationType
from org.xdi.oxauth.service import UserService
from org.xdi.oxauth.service import AuthenticationService
from org.jboss.seam.security import Identity

from oath.google_authenticator import from_b32key

import time
import base64


class PersonAuthentication(PersonAuthenticationType):

    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configAttributes):
        print "OATH authentication initialized."

        return True

    def destroy(self, configAttributes):
        print "OATH destroyed."

        return True

    def getApiVersion(self):
        return 1

    def authenticate(self, configAttributes, requestParams, step):
        userService = UserService.instance()
        authService = AuthenticationService.instance()

        username = requestParams.get('username')[0]
        token = requestParams.get('token')[0]

        if not username or not token:
            print 'Empty input data: username=%s token=%s' % (username, token)
            return False

        # Check if the is user with specified oneid_user_uid
        user_found = userService.getUserByAttribute("username", username)

        if not user_found:
            print "The username %s was not found on the system." % username
            return False

        credentials = Identity.instance().getCredentials()
        credentials.setUsername(username)
        credentials.setUser(user_found)

        secret = base64.b32encode(credentials.getPassword())

        token_generated = from_b32key(secret).generate(t=time.time())

        if int(token) == int(token_generated):
            authService.authenticate(username)
            print "OATH Authentication Successful for %s" % username

        return True

    def prepareForStep(self, configAttributes, requestParams, step):
        return True

    def getExtraParametersForStep(self, configAttributes, step):
        return None

    def getCountAuthenticationSteps(self, configAttributes):
        return 1

    def getPageForStep(self, configAttributes, step):
        return ""

    def logout(self, configAttributes, requestParams):
        return True
