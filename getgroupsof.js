var ldap = require('ldapjs');

var server = 'ldap://bluepages.ibm.com';

if (process.argv.length < 3) {
    console.log("Example usage:\nnode getgroupsof.js user@ibm.com");
    process.exit(0);
}

var emailAddress = process.argv[2];
var search_filter = '(mail=' + emailAddress + ')';
var attribute = 'ibm-allgroups';

var opts = {
    filter: search_filter,
    scope: 'sub',
    timeLimit: 5000,
    attributes: [attribute]
};

var L = ldap.createClient({
    url: 'ldap://bluepages.ibm.com'
});

L.search('o=ibm.com',opts,(error,result) => {
    if (error) {
        console.log("ERROR");
    } else {
        result.on('searchEntry',entry => {
            entry.object[attribute].forEach(group => {
                console.log(group);
            });
        });

        result.on('end',result => {
            process.exit(0);
        });
    }
});

