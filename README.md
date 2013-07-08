api-python
==========

Python API for Conjur.  

Install requirements.txt via pip.  

Put a .conjurpy.cfg in your home dir.

```
(python-2.7)rmdac-cab:src dbernick$ cat ~/.conjurpy.cfg 
[Conjur]
Account: xfx0x
Cas: "authn-xxx-conjur.herokuapp.com"
```

Then run like below.

```
(python-2.7)rmdac-cab:python-2.7 dbernick$ python /Users/dbernick/Code/api-python/src/testscript.py --username dbernick --password 'XXXXXX' -r cas-xxx-conjur.herokuapp.com --login
Testing login: Getting CAS token
service token     : ST-13-XXXXXXX-cas
Conjursecret XXXXXXXXXXXXXXXXXXXXXkw2m3fyxm76x4sk
Authorization: Token token="xxXXXXxxjasfkldsajflkdasjflkjads klfjsadlkfj dskl fjadsklf jlkadsfjlasdkf jsd..asdfasdfasdf"
```

Then the token can be passed to more of the API. Things XXXXed to protect the innocent.
