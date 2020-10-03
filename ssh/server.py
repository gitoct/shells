import socket
import paramiko
import threading
import sys


rsaKey = ""
username = ""
password = ""
clientIP = ""
host_key = paramiko.RSAKey(filename=rsaKey)

class Server (paramiko.ServerInterface):
   def _init_(self):
       self.event = threading.Event()
   def check_channel_request(self, kind, chanid):
       if kind == 'session':
           return paramiko.OPEN_SUCCEEDED
       return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
   def check_auth_password(self, username, password):
       if (username == username) and (password == password):
           return paramiko.AUTH_SUCCESSFUL
       return paramiko.AUTH_FAILED

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((clientIP, 22))
    sock.listen(100)
    print("[*] Listening for incoming connection")
    client, addr = sock.accept()
except Exception, e:
    print("[-] Connection failed: " + str(e))
    sys.exit(1)
print("[+] Connection successful!")

try:
    t = paramiko.Transport(client)
    try:
        t.load_server_moduli()
    except:
        print("[-] Load server moduli failed")
        raise
    t.add_server_key(host_key)
    server = Server()
    try:
        t.start_server(server=server)
    except paramiko.SSHException, x:
        print("[-] SSH failure")

    chan = t.accept(20)
    print("[+] Authenticated connection")
    print chan.recv(1024)
    chan.send('Confirmed')
    command= raw_input("Enter command: ").strip('\n')
    chan.send(command)
    print(chan.recv(1024) + '\n')

except Exception, e:
    print("[-] Exception: " + str(e))
    try:
        t.close()
    except:
        pass
    sys.exit(1)
