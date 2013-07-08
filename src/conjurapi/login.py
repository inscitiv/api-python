'''
Created on Jul 7, 2013

@author: bernz
'''
import ConfigParser,caslib
import os.path
import httplib, urllib, urllib2, cookielib


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
		#print "st     : %s" % (st)
		#print "***"
				
		return st
	except Exception,exc:
		print "CAS login error: %s" % (exc)
		return None
