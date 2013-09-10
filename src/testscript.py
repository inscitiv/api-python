import sys, getopt
from conjurapi.login import login_cas,authenticate,tokenHandler
from conjurapi.Resource import Resource
from conjurapi.clilib import cliauthenticate,clilogin,ConjurConfig
import base64

def main(argv):
    username=""
    password=""
    url = ""
    try:
        opts, args = getopt.getopt(argv,"hnu:p:r:lm",["username=","password=","url=","login","permittedroles"])
    except getopt.GetoptError:
        print "To test login:"
        print 'testscript.py -u casusername -p caspassword -r cashost --login'
        print '--username casusername'
        print '--password caspassword'
        print '--url cashost'
        print 'Functions:'
        print '--login'
        print '--permittedroles'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'testscript.py -u username -p password -r cashost --login'
            print '--username username'
            print '--password password'
            print '--url cashost'
            print 'Functions:'
            print '--login'
            print '--permittedroles'
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-r", "--url"):
            url = arg

    if username==None or password==None or username=="" or password=="":
        print 'need secrets'
        sys.exit()
    else:
        if opt in (" ", "--login"):
            print "Testing login: Getting CAS token"
            try:
                casurl = url
                clilogin(username,password,casurl)
                token = cliauthenticate()
                print "Logged in and Authenticated: %s" % (token)
            except Exception,exc:
                print "Error in test: %s" % (exc)
        elif opt in(" ","--permittedroles"):
            try:
                token = cliauthenticate()
                cfg = ConjurConfig()
                options={
                         "username":username,
                         "account":cfg.getConfVar(var="account"),
                         "stack":cfg.getConfVar(var="stack"),
                }
                res = Resource()
                allroles = res.all_roles(token, options)
                for role in allroles:
                    tokens = role["id"].split(':')[1].split("/")
                    print ("%s")%(role)
            except Exception,exc:
                print "Error in permitted: %s" % (exc)
        else:
            print 'need a function to test (like --login)'
            print 'try -h to see options'
            sys.exit()
            
if __name__ == "__main__":
    main(sys.argv[1:])

#login_cas("dbernick","XXXXXXX","cas.genomebridge.org")
