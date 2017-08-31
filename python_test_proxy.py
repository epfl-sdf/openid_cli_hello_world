import urllib2

opener = urllib2.build_opener(
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.ProxyHandler({'http': 'http://10.92.104.185:8080'}))
urllib2.install_opener(opener)
print urllib2.urlopen('http://www.google.com').read()
