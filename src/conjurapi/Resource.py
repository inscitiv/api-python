'''
Created on Jul 7, 2013

@author: bernz
'''
import ConfigParser,os.path,httplib, urllib, urllib2, cookielib,json
from restkit import request
from .login import ConjurConfig

class Resource:
    
    def all_roles(self,token_encode,options={}):
        cfg = ConjurConfig()
        try:
            gurl = 'https://authz-%s-conjur.herokuapp.com' % (cfg.getStack())
            headers = {"Authorization":token_encode}            
            url = "/%s/roles/user/%s/?all" % (cfg.getAccount(),options["username"])
            r = request(gurl+url, method='GET', headers=headers)
            jsonenv =  json.loads(r.body_string())
            return jsonenv
        except Exception,exc:
            print "Error roles: %s" % (exc)