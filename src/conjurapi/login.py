'''
Created on Jul 7, 2013

@author: bernz
'''
import caslib,os.path,httplib, urllib, urllib2, cookielib,base64,re
from restkit import Resource


def cas_only(username,passwd,casurl=None,serviceurl=None,account=None,prefix=""):
    conaccount = account

    try:
        params = urllib.urlencode({'username': username, 'password': passwd})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPSConnection(casurl,443)
        conn.request("POST", ("%s/v1/tickets/") % (prefix), params, headers)
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
        conn.request("POST", "%s/v1/tickets/%s" % ( prefix,tgt ), params, headers)
        response = conn.getresponse()
        st = response.read()
        conn.close()
        return st
    except Exception,exc:
        print "CAS login error cas_only: %s" % (exc)
        return None

#this logs-in and gets the service token for cas and returns the apikey
def login_cas(username,passwd,casurl=None,account=None,prefix=""):
    conaccount = account
    try:
        service  = 'https://authn-%s-conjur.herokuapp.com/users/login' % (conaccount)
        st = cas_only(username,passwd,casurl,serviceurl=service,account=conaccount,prefix=prefix)        
        bodyurl =  "%s?ticket=%s" % ( service, st )
        cj = cookielib.CookieJar()
        no_proxy_support = urllib2.ProxyHandler({})
        cookie_handler = urllib2.HTTPCookieProcessor(cj)

        opener = urllib2.build_opener(no_proxy_support, cookie_handler, urllib2.HTTPHandler(debuglevel=1))
        urllib2.install_opener(opener)
        protected_data = urllib2.urlopen(bodyurl).read()
        return protected_data
    except Exception,exc:
        print "CAS login error login_cas: %s" % (exc)
        return None
       
#pass api key and username to get a token. Token is usually base64.encodestring'd and put in headers.
def authenticate(username=None,apikey=None,account=None):
    try:
        res = Resource('https://authn-%s-conjur.herokuapp.com' % (account))
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