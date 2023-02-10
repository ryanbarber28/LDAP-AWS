import ldap
import getpass
import re


#Define Connection Parameters
server = input("Enter AD server IP: ")
username = input("Enter admin username: ")
password = getpass.getpass("Enter admin password: ")

# Establish Connection
try:
    ldap_conn = ldap.initialize("ldap://"+server)
    ldap_conn.protocol_version = 3
    ldap_conn.set_option(ldap.OPT_REFERRALS, ldap.OPT_ON)
    ldap_conn.simple_bind_s(username,password)
    print("Authenticated to the AD server successfully")
    
    # Get all users on the AD server
    searchFilter = "(objectClass=user)"
    searchAttribute = ["sAMAccountName", "computer", "givenName", "sn", "distinguishedName", "memberOf"]
    # Extract the domain name from the username
    domain = re.search(r"@([\w]+).([\w]+)", username).group(0)[1:]
    # Seperate the domain name into two parts
    domain_parts = domain.split('.')
    # Construct the search base
    search_base = ','.join(['dc='+x for x in domain_parts])
    result = ldap_conn.search_s(search_base, ldap.SCOPE_SUBTREE, searchFilter, searchAttribute)
    print("All users and computers on the AD server:")
    users_data = []
    for user in result:
        if 'sAMAccountName' in user[1]:
            if user[1]['sAMAccountName'][0].endswith(b'$'):
                user_data = {
                    "type": "Computer",
                    "sAMAccountName": str(user[1]['sAMAccountName'][0]),
                    "distinguishedName": str(user[1]['distinguishedName'][0])
                }
            else:
                user_data = {
                    "type": "User",
                    "sAMAccountName": str(user[1]['sAMAccountName'][0]),
                    "distinguishedName": str(user[1]['distinguishedName'][0])
                }
                if 'givenName' in user[1] and 'sn' in user[1]:
                    user_data["name"] = str(user[1]['givenName'][0]) + " " + str(user[1]['sn'][0])
                if 'memberOf' in user[1]:
                    user_data["memberOf"] = [str(group) for group in user[1]['memberOf']]
            users_data.append(user_data)
    print("Do you want to save the information as a JSON file? (y/n)")
    answer = input()
    if answer.lower() == "y" or answer.lower() == "yes":
        import json
        with open("windowsinfo.json", "w") as f:
            json.dump(users_data, f)
        print("Data saved in windowsinfo.json")
    elif answer.lower() == "n" or answer.lower() == "no":
        for user in users_data:
            if user["type"] == "User":
                print("User: "+user["sAMAccountName"])
                print("Distinguished Name: "+user["distinguishedName"])
                print("Groups: "+", ".join(user["memberOf"]))
                print()
            elif user["type"] == "Computer":
                print("Computer: "+user["sAMAccountName"])
                print("Distinguished Name: "+user["distinguishedName"])
                print()

except ldap.INVALID_CREDENTIALS:
    print("Username or password is incorrect")
except ldap.SERVER_DOWN:
    print("The AD server is not responding")
except Exception as e:
    print("Error: ", e)