from socket import *

serverName = "127.0.0.1"
serverPort = 5312
clientSocket = socket(AF_INET, SOCK_DGRAM)

queryName = "www.example.com"
queryType = b'\x00\x01' # A record query

# Construct DNS query message
message = b'\x11\x22\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' \
          + queryName.encode('utf-8') + b'\x00\x00\x01\x00\x01' \
          + queryType + b'\x00\x00\x00\x00\x00\x00\x00'

# Send DNS query to server
clientSocket.sendto(message, (serverName, serverPort))

# Receive DNS response from server
response, serverAddress = clientSocket.recvfrom(2048)

# Decode DNS response message
responseID = response[:2]
responseCode = response[3] & 15
answerCount = int.from_bytes(response[6:8], byteorder='big')


ip_address = '.'.join(map(str, response[-4:]))

# Print the IP address
print("The response for A request: " + str(ip_address))
# Close socket
clientSocket.close()
