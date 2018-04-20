import socket
import sys
import pprint

# Importing a dynamically generated module

def importCode(code,name,add_to_sys_modules=0):
    """
    Import dynamically generated code as a module. code is the
    object containing the code (a string, a file handle or an
    actual compiled code object, same types as accepted by an
    exec statement). The name is the name to give to the module,
    and the final argument says wheter to add it to sys.modules
    or not. If it is added, a subsequent import statement using
    name will return this module. If it is not added to sys.modules
    import will try to load it in the normal fashion.

    import foo

    is equivalent to

    foofile = open("/path/to/foo.py")
    foo = importCode(foofile,"foo",1)

    Returns a newly generated module.
    """
    import sys,imp
    module = imp.new_module(name)
    exec code in module.__dict__
    if add_to_sys_modules:
        sys.modules[name] = module
    return module

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
try:
    sock.bind(server_address)
except:
    print >>sys.stderr , sock

# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()
print >>sys.stderr, 'connection from', client_address

# Receive module
data = connection.recv(1000)
if data:
   print >>sys.stderr, 'Module received'
   print >>sys.stderr, 'Loading module...'
   module = importCode(data,"test-app", 1)
   module.app.run(host='localhost', port=module.port)
else:
   print >>sys.stderr, 'no data from', client_address
connection.close()



