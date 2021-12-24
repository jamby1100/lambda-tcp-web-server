import json
import socket
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
ip_address = os.getenv("TCP_SERVER_IP_ADDRESS")
port = int(os.getenv("TCP_PORT_NUMBER"))
server_address = (ip_address, port)
sock.connect(server_address)

# Create the data and load it into json
# data = {
#     'cmd': 'test',
#     'data': ['foo', 'bar'],
# }

# msg = '<!DOCTYPE OlsRequestFormat SYSTEM "OlsRequestFormat.dtd">\n<OlsRequestFormat>\n    <FunctionCode>PR</FunctionCode>\n    <ReferenceNo>0001</ReferenceNo>\n    <SourceSystem>SM Advantage</SourceSystem>\n    <CardNumber>202003</CardNumber>\n</OlsRequestFormat>'

msg = '<!DOCTYPE OlsRequestFormat SYSTEM "OlsRequestFormat.dtd">\n<OlsRequestFormat>\n    <FunctionCode>BQ</FunctionCode>\n    <TestMode></TestMode>\n     <ReferenceNo>0001</ReferenceNo>\n    <SourceSystem>BDORW IVRS</SourceSystem>\n    <CardNumber>8880512859925700</CardNumber>\n    <EncryptedPin>0190</EncryptedPin>\n</OlsRequestFormat>'

# msg = json.dumps(data)

# Send the messagett
sock.sendall(msg.encode('utf-8'))

# Receive the message back
res = sock.recv(1024).decode('utf-8')
print("AND THE RESPONSE IS")
print(res)
data = json.loads(res)
print(data)
