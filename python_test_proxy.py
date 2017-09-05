#!/usr/bin/python2.7

import urllib2
import ssl


#urllib2.urlopen("https://your-test-server.local", context=ctx)




#opener = urllib2.build_opener(
#                urllib2.HTTPHandler(),
#                urllib2.HTTPSHandler(),
#                urllib2.ProxyHandler({'https': 'https://10.92.104.172:8080'}))
#urllib2.install_opener(opener)

#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE


proxies = {'https': 'http://10.92.104.172:8080'}
proxy = urllib2.ProxyHandler(proxies)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
handler = urllib2.HTTPSHandler(context=context)
#handler = urllib2.HTTPSHandler()
opener = urllib2.build_opener(proxy, handler)
urllib2.install_opener(opener)



#print urllib2.urlopen('https://www.google.com', context=ctx).read()
print urllib2.urlopen('https://www.google.com').read()
