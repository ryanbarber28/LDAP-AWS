from ldap3 import Server, Connection, ALL

# define the server
s = Server('ldap://192.169.122.20', get_info=ALL)

# define the connection
c = Connection(s, user='cn=administrator,cn=users,dc=Simpsons,dc=local', password='secret')

# bind to the server
if not c.bind():
    print('error in bind', c.result)
else:
    print('bind is successful')

# unbind from the server
c.unbind()