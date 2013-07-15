import sys, getopt
from conjurapi.login import login_cas,authenticate,tokenHandler
from conjurapi import Resource
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
                apikey = login_cas(username,password,url)
                print "Conjur secret %s" % apikey
                token_encode = tokenHandler(authenticate(username,apikey))
                print "Authorization: %s" % token_encode
            except Exception,exc:
                print "Error in test: %s" % (exc)
        elif opt in(" ","--permittedroles"):
            try:
                apikey = login_cas(username,password,url)
                token_encode = tokenHandler(authenticate(username,apikey))
                options={}
                res = Resource()
                res.premitted_roles(token_encode, permission, options)
            except Exception,exc:
                print "Error in test: %s" % (exc)
        else:
            print 'need a function to test (like --login)'
            print 'try -h to see options'
            sys.exit()
            
if __name__ == "__main__":
    main(sys.argv[1:])

#login_cas("dbernick","XXXXXXX","cas-cmi-conjur.herokuapp.com")
