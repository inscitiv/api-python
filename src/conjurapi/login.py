'''
Created on Jul 7, 2013

@author: bernz
'''
import ConfigParser,caslib
import os.path
import httplib, urllib, urllib2, cookielib
from restkit import Resource

class ConjurConfig:
	
	def getAccount(self):
		config = ConfigParser.ConfigParser()
		try:
			config.read(os.path.expanduser("~")+'/.conjurpy.cfg')
			return config.get('Conjur', 'Account')
		except Exception,e:
			config.read('conjur.py.example')
			return config.get('Conjur', 'Account')

	def getCas(self):
		config = ConfigParser.ConfigParser()
		try:
			config.read(os.path.expanduser("~")+'/.conjurpy.cfg')
			return config.get('Conjur', 'Cas')
		except Exception,e:
			config.read('conjur.py.example')
			return config.get('Conjur', 'Cas')


def login_cas(username,passwd,casurl=None):
	cfg = ConjurConfig()
	if casurl==None:
		casurl = cfg.getCas()
	
	try:
		params = urllib.urlencode({'username': username, 'password': passwd})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = httplib.HTTPSConnection(casurl,443)
		conn.request("POST", "/v1/tickets/", params, headers)
		response = conn.getresponse()
		data = response.read()
		location = response.getheader('location')
		if not location:
			raise Exception("Didn't get anything back from CAS request. Username or Password wrong?")
		#  Pull off the TGT from the end of the location, this works for CAS 3.3-FINAL
		tgt = location[location.rfind('/') + 1:]
		conn.close()
		#return tgt
		
		service  = 'https://authn-%s-conjur.herokuapp.com/users/login' % (cfg.getAccount())
		params = urllib.urlencode({'service': service })
		conn = httplib.HTTPSConnection(casurl,443)
		conn.request("POST", "/v1/tickets/%s" % ( tgt ), params, headers)
		response = conn.getresponse()
		st = response.read()
		conn.close()

		#print "service: %s" % (service)
		print "service token     : %s" % (st)
		#print "***"
		bodyurl =  "%s?ticket=%s" % ( service, st )

		cj = cookielib.CookieJar()
		# no proxies please
		no_proxy_support = urllib2.ProxyHandler({})
		# we need to handle session cookies AND redirects
		cookie_handler = urllib2.HTTPCookieProcessor(cj)

		opener = urllib2.build_opener(no_proxy_support, cookie_handler, urllib2.HTTPHandler(debuglevel=1))
		urllib2.install_opener(opener)
		protected_data = urllib2.urlopen(bodyurl).read()
		#print protected_data				
		return protected_data
	except Exception,exc:
		print "CAS login error: %s" % (exc)
		return None

def authenticate(username,apikey):
        cfg = ConjurConfig()

	try:
		res = Resource('https://authn-%s-conjur.herokuapp.com' % (cfg.getAccount()))
                url = "/users/%s/authenticate" % username
                params = {}
                headers = {"Accept": "text/plain"}
		r=res.post(url,payload=apikey,headers=headers,params_dict=params)
                print r.body_string()
		#data = response.read()
	except Exception,exc:
		print "Error authenticate: %s" % (exc)

