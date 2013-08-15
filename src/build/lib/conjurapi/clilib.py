import login,os
from .login import login_cas,tokenHandler,authenticate,ConjurConfig

def delete_credentials():
    try:
        cfg = ConjurConfig()
        url = cfg.getUrl()
        cfg = ConjurConfig()
        cfg.delCredential(url)
    except Exception,exc:
        raise "Could not delete creds: "+exc

def clilogin(username,password,casurl):
    apikey = login_cas(username,password,casurl)
    delete_credentials()
    cfg = ConjurConfig()
    cfg.newCredential(cfg.getUrl(), username, apikey)

def cliauthenticate():
    cfg = ConjurConfig()
    cred = cfg.getCredential(cfg.getUrl())
    token_encode = tokenHandler(authenticate(cred["login"],cred["apikey"]))
    return token_encode
    
