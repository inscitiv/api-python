'''
Created on Jul 7, 2013

@author: bernz
'''
import ConfigParser,caslib,os.path,httplib, urllib, urllib2, cookielib,base64
from restkit import Resource
from yaml import load

class ConjurConfig:
    
    def getAccount(self):
        #config = ConfigParser.ConfigParser()
        try:
            config = load(file(os.path.expanduser("~")+'/.conjurrc','r'))
            #config = ConfigObj(os.path.expanduser("~")+'/.conjurrc',configobj.pref_dict)
            #config.read(os.path.expanduser("~")+'/.conjurrc')
            #return config.get('Conjur', 'account')[0]
            return config.get('account')
        except Exception,e:
            raise Exception("Need valid conjurrc: %s" % (e))
            #config.read('conjur.py.example')
            #return config.get('Conjur', 'account')[0]

    def getUrl(self):
        #config = ConfigParser.ConfigParser()
        try:
            config = load(file(os.path.expanduser("~")+'/.conjurrc','r'))
            #config.read(os.path.expanduser("~")+'/.conjurrc')
            #return config.get('Conjur', 'account')[0]
            return config.get('url')
        except Exception,e:
            raise Exception("Need valid conjurrc")
            #config.read('conjur.py.example')
            #return config.get('Conjur', 'account')[0]
    
    def getCas(self):
        #config = ConfigParser.ConfigParser()
        try:
            config = load(file(os.path.expanduser("~")+'/.conjurrc','r'))
            #config.read(os.path.expanduser("~")+'/.conjurrc')
            #return config.get('Conjur', 'account')[0]
            return config.get('cas')
        except Exception,e:
            raise Exception("Need valid conjurrc")
            #config.read('conjur.py.example')
            #return config.get('Conjur', 'account')[0]
                       
    def getStack(self):
        #config = ConfigParser.ConfigParser()
        try:
            config = load(file(os.path.expanduser("~")+'/.conjurrc','r'))
            #config.read(os.path.expanduser("~")+'/.conjurrc')
            #return config.get('Conjur', 'account')[0]
            return config.get('stack')
        except Exception,e:
            raise Exception("Need valid conjurrc")
            #config.read('conjur.py.example')
            #return config.get('Conjur', 'account')[0]


#this logs-in and gets the service token for cas and returns the apikey
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
        #print "service token     : %s" % (st)
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
       
#pass api key and username to get a token. Token is usually base64.encodestring'd and put in headers.
def authenticate(username,apikey):
    cfg = ConjurConfig()
    try:
        res = Resource('https://authn-%s-conjur.herokuapp.com' % (cfg.getAccount()))
        url = "/users/%s/authenticate" % username
        params = {}
        headers = {"Accept": "text/plain"}
        r=res.post(url,payload=apikey,headers=headers,params_dict=params)
        return r.body_string()
    except Exception,exc:
        print "Error authenticate: %s" % (exc)
        
def tokenHandler(token):
    token_encode = base64.encodestring(token)
    return "Token token=\"%s\" " % token_encode