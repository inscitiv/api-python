import login,os,ConfigParser
from .login import login_cas,tokenHandler,authenticate
from yaml import load

class ConjurConfig:

    def getConfVar(self,var=None,conffile=None):
        config = None
        if not conffile:
            config = load(file(os.path.expanduser("~")+'/.conjurrc','r'))
        try:
            if not config:
                config = load(file(conffile,'r'))
            return config.get(var)
        except Exception,e:
            raise Exception("Need valid conjurrc: %s %s" % (e,var))        
    
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

def delete_credentials():
    try:
        cfg = ConjurConfig()
        url = cfg.getConfVar(var="url")
        cfg.delCredential(url)
    except Exception,exc:
        raise "Could not delete creds: "+exc

def clilogin(username,password,casurl):
    cfg = ConjurConfig()
    apikey = login_cas(username,password,casurl,account=cfg.getConfVar(var="account"),prefix="/cmi-cas")
    print apikey
    delete_credentials()
    cfg.newCredential(cfg.getConfVar(var="url"), username, apikey)
    return cfg.getCredential(cfg.getConfVar(var="url"))

def cliauthenticate(account=None):
    cfg = ConjurConfig()
    cred = cfg.getCredential(cfg.getConfVar(var="url"))
    token_encode = tokenHandler(authenticate(cred["login"],cred["apikey"],cfg.getConfVar(var="account")))
    return token_encode
    
