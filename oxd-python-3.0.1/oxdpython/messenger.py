import json
import socket
import logging

from collections import namedtuple

logger = logging.getLogger(__name__)


class Messenger:
    """A class which takes care of the socket communication with oxD Server.
    The object is initialized with the port number
    """
    def __init__(self, port=8099):
        """Constructor for Messenger

        Args:
            port (integer) - the port number to bind to the localhost, default
                             is 8099
        """
        self.host = 'localhost'
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug("Creating a AF_INET, SOCK_STREAM socket.")
        self.firstDone = False

    def __connect(self):
        """A helper function to make connection."""
        try:
            logger.debug("Socket connecting to %s:%s", self.host, self.port)
            self.sock.connect((self.host, self.port))
        except socket.error as e:
            logger.exception("socket error %s", e)
            logger.error("Closing socket and recreating a new one.")
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))

    def __json_object_hook(self, d):
        """function to customized the json.loads to return named tuple instead
        of a dict"""
        return namedtuple('response', d.keys())(*d.values())

    def __json2obj(self, data):
        """Helper function which converts the json string into a namedtuple
        so the reponse values can be accessed like objects instead of dicts"""
        return json.loads(data, object_hook=self.__json_object_hook)

    def send(self, command):
        """send function sends the command to the oxD server and recieves the
        response.

        Args:
            command (dict) - Dict representation of the JSON command string

        Returns:
            response (dict) - The JSON response from the oxD Server as a dict
        """
        cmd = json.dumps(command)
        cmd = "{:04d}".format(len(cmd)) + cmd
        msg_length = len(cmd)

        # make the first time connection
        if not self.firstDone:
            logger.info('Initiating first time socket connection.')
            self.__connect()
            self.firstDone = True

        # Send the message the to the server
        totalsent = 0
        while totalsent < msg_length:
            try:
                logger.debug("Sending: %s", cmd[totalsent:])
                sent = self.sock.send(cmd[totalsent:])
                totalsent = totalsent + sent
            except socket.error as e:
                logger.exception("Reconneting due to socket error. %s", e)
                self.__connect()
                logger.info("Reconnected to socket.")

        # Check and recieve the response if available
        parts = []
        resp_length = 0
        recieved = 0
        done = False
        while not done:
            part = self.sock.recv(1024)
            if part == "":
                logger.error("Socket connection broken, read empty.")
                self.__connect()
                logger.info("Reconnected to socket.")

            # Find out the length of the response
            if len(part) > 0 and resp_length == 0:
                resp_length = int(part[0:4])
                part = part[4:]

            # Set Done flag
            recieved = recieved + len(part)
            if recieved >= resp_length:
                done = True

            parts.append(part)

        response = "".join(parts)
        # return the JSON as a namedtuple object
        return self.__json2obj(response)
