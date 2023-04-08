from socket import *

# Specifying the port and ip
port = 5312
ip = '127.0.0.1'

# Initialize IPv4 and UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((ip, port))

# Display a message to indicate that the server is running
print("DNS server is running...")

# Define a dictionary to store DNS mappings
dns_mapping = {
    'www.example.com': {'A': '192.168.121.33', 'CNAME': 'example.com'},
    'www.google.com': {'A': '172.217.6.238', 'CNAME': 'google.com'},
    'www.spotify.com': {'A': '35.186.224.25', 'CNAME': 'spotify.com'},
    'www.facebook.com': {'A': '69.63.176.13', 'CNAME': 'facebook.com'},
    'www.youtube.com': {'A': '208.65.153.238', 'CNAME': 'youtube.com'}
}

while True:
    # Receive query from client
    query, clientAddress = serverSocket.recvfrom(2048)

    # Extract the query name and type from the DNS query message
    queryName = query[12:].decode('utf-8').split('\x00')[0]
    queryType = query[28:30]

    # Construct the DNS response message
    if queryName in dns_mapping:
        if queryType == b'\x00\x01':  # A record query
            ipAddress = dns_mapping[queryName]['A']
            response = b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00' \
                       + query[12:] + b'\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x05\x59\x00\x04' \
                       + inet_aton(ipAddress)
        elif queryType == b'\x00\x05':  # CNAME query
            cname = dns_mapping[queryName]['CNAME']
            response = b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00' \
                       + query[12:] + b'\x00\x00\x05\x00\x01\xc0\x0c\x00\x05\x00\x01\x00\x00\x04\x68\x00\x08' \
                       + cname.encode('utf-8')

        # Send the DNS response back to the client
        serverSocket.sendto(response, clientAddress)
