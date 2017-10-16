import ldap
import sys

if len(sys.argv) != 2:
    print "USAGE: python ldap_search.py 'John C. Doe'"
    sys.exit(1)

ident = sys.argv[1]
L = ldap.initialize('ldap://bluepages.ibm.com')
L.protocol_version = ldap.VERSION3
L.set_option(ldap.OPT_REFERRALS,0)

try:
    L.simple_bind_s()

    basedn = 'o=ibm.com'
    searchScope = ldap.SCOPE_SUBTREE
    #filter = '(mail=aparicdd@ph.ibm.com)'
    filter = '(cn=%s)' % ident
    searchKey = 'mail'

    ldap_result_id = L.search_s(basedn,searchScope,filter,[searchKey])
    nfo_tuple = ldap_result_id[0]
    searchValue = nfo_tuple[1][searchKey]

    print searchValue
except:
    print "error"
