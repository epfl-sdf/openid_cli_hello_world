import logging

from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError

logger = logging.getLogger(__name__)


class Configurer(object):
    """The class which holds all the information about the client and the OP
    metadata"""
    def __init__(self, cfg_file):
        self.parser = SafeConfigParser()
        self.config_file = cfg_file
        self.parser.read(self.config_file)
        logger.info("Loading config at: %s", cfg_file)

    def get(self, section, key):
        """get function reads the config value for the requested section and
        key and returns it

        Args:
            section (string) - the section to look for the config value
                               either - oxd, client
            key (string) - the key for the config value required

        Returns:
            value (string) - the function returns the value of the key
                               in the appropriate format if found or returns
                               None if such a section or key couldnot be found

        Example:
            config = Configurer(location)
            oxd_port = config.get('oxd', 'port')  # returns the port of the oxd
        """
        try:
            return self.parser.get(section, key)
        except (NoOptionError, NoSectionError) as e:
            logger.warning("%s", e)
            return None

    def set(self, section, key, value):
        """set function sets a particular value for the specified key in the
        specified section and writes it to the config file.

        Args:
            section (string) - the section under which the config should be
                               saved. Only accepted values are - oxd, client

            key (string) - the key/name of the config value

            value (string) - the value which needs to be stored as a string

        Returns:
            success (bool) - a boolean indication of whether the value was
                             stored successfully in the file
        """
        if not self.parser.has_section(section):
            logger.warning("Invalid config section: %s", section)
            return False

        self.parser.set(section, key, value)

        with open(self.config_file, 'wb') as cfile:
            self.parser.write(cfile)

        return True
