# oxD Python Demo site

This is a demo site for oxd-python written using Python Flask to demonstrate how to use oxd-python to perform authorization with an OpenID Provider and fetch information.

## Deployment

### Prerequisites

Ubuntu 14.04 with some basic utilities listed below

```bash
apt-get install apache2 libapache2-mod-wsgi python-dev git python-pip
a2enmod wsgi
a2enmod ssl
```

###Gluu Development Binaries

```bash
echo "deb http://repo.gluu.org/ubuntu/ trusty-devel main" > /etc/apt/sources.list.d/gluu-devel-repo.list
curl http://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
apt-get update
apt-get install gluu-oxd-server
```

### Configuring the oxd-server

Edit the file `/opt/oxd-server/conf/oxd-default-site-config.json`

* Set the OP HOST name to your OpenID Provider domain at the line `"op_host": ""`
* Change the `response_types` line to `"response_types": ["code"]`

Start the oxd-server
```bash
service gluu-oxd-server start
```

## Demosite deployment

OpenID Connect works only with HTTPS connections. So let us get the ssl certs ready
```bash
mkdir /etc/certs
cd /etc/certs
openssl genrsa -des3 -out demosite.key 2048
openssl rsa -in demosite.key -out demosite.key.insecure
mv demosite.key.insecure demosite.key
openssl req -new -key demosite.key -out demosite.csr
openssl x509 -req -days 365 -in demosite.csr -signkey demosite.key -out demosite.crt
```

Get the source code for demosite

```bash
cd /var/www/html
git clone https://github.com/GluuFederation/oxd-python.git
```

Deploying the site

```bash
cd oxd-python
pip install flask
cp demosite/demosite.conf /etc/apache2/sites-available/demosite.conf
chown www-data demosite/demosite.cfg
a2ensite demosite
service apache2 restart
```
Now the site would be available as the default site for https (port 443) at your domain.
However the callback urls need to be configured before you can see things working.
Edit `demosite/demosite.cfg` and change the redirect uris for yor domain. **OR** If you are testing
at a local server then you can add `client.example.com` to you `/etc/hosts` to point to your
IP, instead of editing the uris in the `demosite.cfg` file.
