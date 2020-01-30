import socket 
import json
from threading import Thread 
from socketserver import ThreadingMixIn 
import geopandas
from shapely.ops import nearest_points
from shapely.geometry import Point

servers = []
servers_connections = []

def find_nearest_server(user, servers):
    ###find the nearest server to the client based on lat and long
    if not servers:
        return None
    gdf = geopandas.GeoDataFrame(servers, columns=['ip','port', 'longitude','latitude', 'geometry'])
    multipoint = gdf.geometry.unary_union
    queried_geom, nearest_geom = nearest_points(user, multipoint)
    for index, row in gdf.iterrows():
        if row.geometry == nearest_geom:
            nearest_server = {
                "ip": row.ip,
                "port": row.port,
                "longitude": row.longitude,
                "latitude": row.latitude
            }
            return nearest_server

class ClientThread(Thread):
    ###Thread that listens to clients and regional servers
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print (f'New socket thread started for: {ip}:{str(port)}')
 
    def run(self):
        global servers 
        global servers_connections
        while True :
            try: 
                ###listen for messages and checks if it's a user, a server or a broadcast message
                message_received = conn.recv(2048)
                message_received = json.loads(message_received.decode('utf8'))
                if message_received['type'] == 'server':
                    ###add the server to the list of regional servers and connections available
                    current_server = [message_received['ip'], message_received['port'], message_received['longitude'], message_received['latitude'],Point(message_received['longitude'], message_received['latitude'])]
                    servers.append(current_server)
                    servers_connections.append({
                        "id": message_received['id'],
                        "connection": conn
                    })
                    conn.send(str.encode('Connected'))
                elif message_received['type'] == 'client':
                    ###finds the nearest server to the client, returns it and closes the connection
                    nearest_server = find_nearest_server(Point(message_received['longitude'], message_received['latitude']),servers)
                    if not nearest_server:
                        nearest_server = 'No server available.'
                    conn.send(str.encode(json.dumps(nearest_server)))
                    break
                elif message_received['type'] == 'set':
                    ###Gets a broadcast message, then sends it to all servers except the one that generates it
                    for server in servers_connections:
                        if server['id'] != message_received['sender']:
                            server['connection'].send(str.encode(json.dumps(message_received)))
            except json.decoder.JSONDecodeError:
                continue

###master server's info
master_ip = '10.230.4.253' 
master_port = 5555
master_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
master_server.bind((master_ip, master_port)) 
threads = [] 
#waits for connections and send each one to a thread
while True:
    master_server.listen(5) 
    print ("Waiting for connections ...")
    (conn, (ip,port)) = master_server.accept() 
    new_thread = ClientThread(ip,port) 
    new_thread.start() 
    threads.append(new_thread) 
 
for t in threads: 
    t.join() 