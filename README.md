# Ormuco

Geo Distributed LRU:

Everything was made with Python 3, use requirements file to get all the libraries needed.

The master script creates the main server, this server will coordinate all the other regional servers that holds the data, also it will provide the users with the nearest regional server based on their coordinates, and propagate the data between servers.



The master server will listen to any connections, if a regional server connects it will receive the server's info, IP, PORT, LAT and LONG (ideally this information would come from the network configurations of the server, since this is a local development it's necessary to add the local address manually and use a different port for every server created). After a succesful connection the master server will add the regional server to a list of available servers for any user to connect.



When a user connects to the master server, the user will send his/her location in order to get the closest server if there's any. For the distance between servers and users I have used geopandas for the calculation. 

After that the connection to the master server is closed and the user connects to the regional server that was indicated. When the connection to the regional server is succesful it asks for the action to executed, get or set. 



If the user selects "set" the system will ask for the data to be stored in the format key:value. After the user sets the info the regional server will store the data into the local variable real_data and make the proper changes to the cache. This data is then propagated to the other regional servers in order to have consistent data across all servers.



If the user selects "get" the system will ask for the key of the data that is needed, the regional server checks in the current cache for the data and checks for expiration time, this time is a value set in seconds at the beginning of the server creation. If the server cannot find the data in the cache then checks the real_data variable, if exits then refreshes the value in the cache, and retrieves the value, if the value not exists then notifies the user.

