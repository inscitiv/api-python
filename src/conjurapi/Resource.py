'''
Created on Jul 7, 2013

@author: bernz
'''
import json
from restkit import request

class Resource:
    
    def all_roles(self,token_encode,options={}):
        try:
            gurl = 'https://authz-%s-conjur.herokuapp.com' % (options["stack"])
            headers = {"Authorization":token_encode}            
            url = "/%s/roles/user/%s/?all" % (options["account"],options["username"])
            r = request(gurl+url, method='GET', headers=headers)
            jsonenv =  json.loads(r.body_string())
            return jsonenv
        except Exception,exc:
            print "Error roles: %s" % (exc)
