'''
Created on Jul 7, 2013

@author: bernz
'''
import ConfigParser,caslib,os.path,httplib, urllib, urllib2, cookielib,base64,re
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
    
    def newCredential(self,machine,username,password):
        config = ConfigParser.ConfigParser()
        try:
            #config = load(file(os.path.expanduser("~")+'/.conjurrc','r'))
            #config.read(os.path.expanduser("~")+'/.conauth')
            config.add_section(machine)
            config.set(machine, 'login', username)
            config.set(machine, 'apikey', password)
            # Writing our configuration file to 'example.cfg'
            with open(os.path.expanduser("~")+'/.conauth', 'wb') as configfile:
                config.write(configfile)
        except Exception,e:
            raise Exception("Need valid .conauth")

    def delCredential(self,machine):
        config = ConfigParser.RawConfigParser()
        try:
            config.read(os.path.expanduser("~")+'/.conauth')
            try:
                config.remove_section(machine)
                with open(os.path.expanduser("~")+'/.conauth', 'wb') as configfile:
                    config.write(configfile)
            except:
                pass            
        except Exception,e:
            raise Exception("Can't delete %s" % e)

    def getCredential(self,machine):
        config = ConfigParser.RawConfigParser()
        try:
            config.read(os.path.expanduser("~")+'/.conauth')
            try:
                login = config.get(machine, 'login')
                apikey = config.get(machine, 'apikey')
                return {
                        "login":login,
                        "apikey":apikey
                        }
            except Exception,e:
                raise Exception("Need to re-login")
        except Exception,e:
            raise Exception("Need valid .conauth or need to login: %s" % e)
            return None

def cas_only(username,passwd,casurl=None,serviceurl=None,account=None):
    cfg = ConjurConfig()
    if casurl==None:
        casurl = cfg.getCas()
    conaccount =""
    try:
        conaccount = cfg.getAccount()
    except:
        conaccount = account    

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
        service=""
        if serviceurl:
            service = serviceurl
        else:
            service  = 'https://authn-%s-conjur.herokuapp.com/users/login' % (conaccount)
        params = urllib.urlencode({'service': service })
        conn = httplib.HTTPSConnection(casurl,443)
        conn.request("POST", "/v1/tickets/%s" % ( tgt ), params, headers)
        response = conn.getresponse()
        st = response.read()
        conn.close()
        return st
    except Exception,exc:
        print "CAS login error: %s" % (exc)
        return None

#this logs-in and gets the service token for cas and returns the apikey
def login_cas(username,passwd,casurl=None,account=None):
    cfg = ConjurConfig()
    if casurl==None:
        casurl = cfg.getCas()
    conaccount =""
    try:
        conaccount = cfg.getAccount()
    except:
        conaccount = account            
    try:
        service  = 'https://authn-%s-conjur.herokuapp.com/users/login' % (conaccount)
        st = cas_only(username,passwd,casurl)        
        bodyurl =  "%s?ticket=%s" % ( service, st )
        cj = cookielib.CookieJar()
        no_proxy_support = urllib2.ProxyHandler({})
        cookie_handler = urllib2.HTTPCookieProcessor(cj)

        opener = urllib2.build_opener(no_proxy_support, cookie_handler, urllib2.HTTPHandler(debuglevel=1))
        urllib2.install_opener(opener)
        protected_data = urllib2.urlopen(bodyurl).read()
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
    token_encode = base64.urlsafe_b64encode(token)
    t = token_encode
    #t2 = re.sub("\n", "", t)
    return "Token token=\"%s\"" % t