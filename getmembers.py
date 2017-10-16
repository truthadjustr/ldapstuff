import ldap
import sys
import datetime
import os
import redis
import sys

if len(sys.argv) != 2:
    print "USAGE: python getmembers.py BLUE_GROUP_NAME_HERE"
    sys.exit(1)

bluegroup = sys.argv[1]

redis_host = os.getenv("REDIS_HOST")
redis_pass = os.getenv("REDIS_PASS")

if redis_host and redis_pass: 
    cache = redis.Redis(host = redis_host,password = redis_pass,db = 4)
else:
    cache = None

L = ldap.initialize('ldap://bluepages.ibm.com')
L.protocol_version = ldap.VERSION3
L.set_option(ldap.OPT_REFERRALS, 0)

#basedn  = "cn=DST,ou=memberlist,ou=ibmgroups,o=ibm.com"
basedn  = "cn=%s,ou=memberlist,ou=ibmgroups,o=ibm.com" % bluegroup

searchAttribute = None
searchScope = ldap.SCOPE_SUBTREE
Filter = '(objectClass=*)'

try:
    L.simple_bind_s()
    ldap_result_id3 = L.search_s(basedn, searchScope, Filter)
    nfo_tuple3 = ldap_result_id3[0]

    for memberuid in nfo_tuple3[1]['uniquemember']:
        basedn = memberuid
        ldap_result2_id = L.search_s(basedn, searchScope, Filter)
        nfo_tuple2 = ldap_result2_id[0]
        memberinfo = nfo_tuple2[1]

        # 'emailAddress' key is not guaranteed
        if isinstance(memberinfo['mail'],list):
            emailaddr = ';'.join(memberinfo['mail']) 
        else:
            emailaddr = memberinfo['mail'] 

        # handle a certain quirks in IBM LDAP
        notesId = ''
        for e in ['notesid','notesId','notesemail','notesEmail']: 
            if e in memberinfo:
                notesId = memberinfo[e][0]
                break

        role = ''
        for role_field in ['jobresponsibilities','jobResponsibilities']:
            field_type = memberinfo.get(role_field)
            if field_type is not None:
                if isinstance(field_type,list):
                    role = memberinfo.get(role_field,[''])[0]
                    break
                elif isinstance(field_type,str):
                    role = memberinfo.get(role_field)
                    break

        memberdata = { 'notesEmail': notesId, 'mail': emailaddr,'role': role }
        if cache:
            if not cache.sismember(DstGroup,memberdata):
                cache.sadd(DstGroup,memberdata)
        else:
            print memberdata

except ldap.FILTER_ERROR,e:
    print "filter error"
except ldap.INVALID_CREDENTIALS:
    print "Your username or password is incorrect."
    sys.exit(1)
except ldap.LDAPError, e:
    if type(e.message) == dict and e.message.has_key('desc'):
        print e.message['desc']
    else: 
        print e
    sys.exit(2)
