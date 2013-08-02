'''
Created on Jul 7, 2013

@author: bernz
'''
import ConfigParser,caslib,os.path,httplib, urllib, urllib2, cookielib
from restkit import Resource
from .login import ConjurConfig

class Resource:

    def permitted_roles(self, token_encode, options = {}):
        cfg = ConjurConfig()
        try:
            res = Resource('https://authn-%s-conjur.herokuapp.com' % (cfg.getStack()))
            #url = "/users/%s/authenticate" % username
            url = "/%s/roles/allowed_to/%s/%s/%s" % (cfg.getAccount(),
                                                     options["permission"],
                                                     options["kind"],
                                                     options["identifier"])
            params = {}
            headers = {"Accept": "text/plain",
                       "Authorization":token_encode}
            r=res.get(url,headers=headers,params_dict=params)
            return r.body_string()
        except Exception,exc:
            print "Error permitted: %s" % (exc)
        
        #JSON.parse 
        #RestClient::Resource.new(Conjur::Authz::API.host, self.options)
        #["#{account}/roles/allowed_to/#{permission}/#{path_escape kind}/#{path_escape identifier}"]
        #.get(options)
