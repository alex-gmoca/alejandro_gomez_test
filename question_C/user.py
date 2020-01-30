import socket 
import json
import re
import time

def get_nearest_server():
	#connects to master server to receive the nearest server
	host = '10.230.4.253' 
	port = 5555
	client_latitude = input("Client's latitude: ")
	client_longitude = input("Client's longitude: ")
	user_data = {
	    "type": "client",
	    "latitude": float(client_latitude),
	   	"longitude": float(client_longitude)
	}
	master_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	master_server.connect((host, port))
	master_server.send(str.encode(json.dumps(user_data)))     
	nearest_server = master_server.recv(1024)
	print(f'connected to: {nearest_server}')
	master_server.close() 
	return nearest_server

try:
	#gets nearest server and connects
	nearest_server = json.loads(get_nearest_server())
	rg_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	rg_server.connect((nearest_server['ip'], 5554))
except KeyError:
	print('No available servers.')
else:
	data = None
	action = ''
	server_data = {}
	#prompts user for the desired action get or set
	while not re.match("set|SET|Set|get|Get|GET", action):
		action = input('set or get?: ')
	if re.match("set|SET|Set", action):
		#prompts the user to insert Key and Value to set
		while not data:
			data = input('Insert key:value ')
			data = re.match("(\w+):(\w+)", data)
		server_data = {
			"type": "set",
			"key": data[1],
			"value": data[2]
		}
	else:
		#prompts the user to insert the key to get
		while not data:
			data = input('Key to get?: ')
		server_data = {
			"type": "get",
			"key": data,
		}
	#send the action and the values to the regional server
	rg_server.send(str.encode(json.dumps(server_data)))
	print(rg_server.recv(1024))
	rg_server.close() 