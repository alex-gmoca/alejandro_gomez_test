import socket 
import json
from cache import cacheLRU
from threading import Thread 
from socketserver import ThreadingMixIn 
from uuid import uuid4

class MasterThread(Thread):
	#thread listening to master server for any broadcast
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		global cache
		global real_data
		while True:
			data = master_server.recv(1024)
			if data != b'':
				try:
					#takes data created in other server and stores it here
					data = json.loads(data)
					cache.set(data['key'], data['value'])
					real_data[data['key']] = data['value']
				except json.decoder.JSONDecodeError:
					continue

class ClientThread(Thread): 
	#thread listening to clients for any set or get operation
	def __init__(self,ip,port): 
		Thread.__init__(self) 
		self.ip = ip 
		self.port = port
 
	def run(self):
		while True:
			global real_data
			global cache
			global server_data 
			client_message_received = cl_conn.recv(2048)
			try:
				client_message_received = json.loads(client_message_received.decode('utf8'))
				if client_message_received['type'] == 'set':
					###set data in cache and real storage
					cache.set(client_message_received['key'], client_message_received['value'])
					real_data[client_message_received['key']] = client_message_received['value']
					item = 'Done'
					###send it to master to bradcast it to other servers
					global master_server
					client_message_received['sender'] = server_data['id']
					master_server.send(str.encode(json.dumps(client_message_received)))
				elif client_message_received['type'] == 'get':
					###search the cache for the item
					item = cache.get(client_message_received['key'])
					if not item:
						###if not found in cache find it in the real data storage
						item = real_data.get(client_message_received['key'],None)
						if item:
							cache.set(client_message_received['key'], item)
							item = json.dumps(item)
						else:
							item = 'Item not found.'
				cl_conn.send(str.encode(item))
			except json.decoder.JSONDecodeError:
				break


threads = []
master_host = '10.230.4.253'
master_port = 5555
#getting manually the server's info, in prod this info could be obtained from network configurations.
input_ip = input("Server's IP: ")
input_port = input("Server's port: ")
input_latitude = input("Server's Latitude: ")
input_longitude = input("Server's Longitude: ")
server_data = {
	"id": str(uuid4()),
    "type": "server",
    "latitude": float(input_latitude),
    "longitude": float(input_longitude),
    "ip": input_ip,
    "port": int(input_port)
}
#connects to master to let it know that this server is available
master_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
master_server.connect((master_host, master_port))
master_server.send(str.encode(json.dumps(server_data)))     
print(master_server.recv(1024))
master_thread = MasterThread()
master_thread.start()
threads.append(master_thread)
real_data = {}
###cache creation, first parameter is the number of elements in cache, the second is the expiration time is in seconds
cache = cacheLRU(5,15)
rg_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
rg_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
rg_server.bind((server_data['ip'], server_data['port'])) 
while True:
	#debug prints to see the info in this server
    #print(real_data)
    #print(cache.cache)
    rg_server.listen(5) 
    print ("Waiting for client connections ...")
    (cl_conn, (cl_ip, cl_port)) = rg_server.accept() 
    cl_newthread = ClientThread(cl_ip, cl_port) 
    cl_newthread.start() 
    threads.append(cl_newthread) 
 
for t in threads: 
    t.join() 
master_server.close() 