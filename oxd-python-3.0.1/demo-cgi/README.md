## Demo CGI

CGI scripts are the simplest possible Web applications. The goal of 
these scripts is to show oxd-python at work with a minimal amount of 
application overhead. A cookie is used to track a session id, which 
is persisted using the simple python shelve database interface.

This sample consists of the following files

* **demosite.cfg** This file contains the callback urls and other site 
specific settings
* **home.cgi** This is the main page of the app. Navigate to this page 
first. 
* **redirect-to-login.cgi** This script redirects the user to the 
OpenID Connect login (if no sessioin exists) and authorization pages.
* **callback-login.cgi** This script uses the authorization code to 
obtain user information, and create a session.
* **redirect-to-logout.cgi** This script sends the person to the 
OpenID Connect logout page. 
* **callback-logout.cgi** This page is called for OpenID Connect
front channel logout. It clears the session and cookie, and redirects
to the logout confirmation page
* **logout-confirmation.cgi** This pages checks to make sure that the
cookie and DB session are removed.
* **setupDemo.py** Helper script used to create the DB and set 
file permissions.
* **appLog.py** Module to centralize logging code
* **constants.py** Module to centralize constant values

## Deployment of demosite in Ubuntu

1. Install [oxd-server](https://gluu.org/docs/oxd/install/)
2. Edit `/opt/oxd-server/conf/oxd-conf.json` and enter your OXD License details. Edit `/opt/oxd-server/conf/oxd-default-site-conf.json` and enter the value for `op_host` pointing to your Gluu Server installation. Run `service gluu-oxd-server start`
3. Install oxd-python
    ```
    apt-get install python-pip
    pip install oxdpython
    ```
3. Install and configure Apache 2
    ```
    apt-get install apache2
    a2enmod cgi
    a2enmod ssl
    a2dissite 000-default
    a2ensite default-ssl
    ```
2. Clone the demosite and setup for cgi-bin
    ```
    cd /usr/lib/cgi-bin/
    wget https://github.com/GluuFederation/oxd-python/archive/v3.0.1.tar.gz
    tar -xvf v3.0.1.tar.gz
    cp oxd-python-3.0.1/demo-cgi/* .
    chmod +x *.cgi
    ```
3. Edit `COOKIE_DOMAIN` in `constants.py` to suit your domain name.
4. Setup logging and initialize the app
    ```
    mkdir -p /var/log/sampleapp/
    python setupDemo.py
    ```
4. Change the domain names in `/var/log/sampleapp/demosite.cfg` URLs to match yours. (Similar to Step 3)
5. Visit `https://your-hostname/cgi-bin/home.cgi`
6. To debug check the logs are `/var/log/sampleapp/app.log` and `/var/log/oxd-server.log`

See the sequence diagram below to get a better picture of the flow of 
this application.

![Demo Sequence Diagram](https://raw.githubusercontent.com/GluuFederation/oxd-python/master/demo-cgi/sequence_diagram.png)
