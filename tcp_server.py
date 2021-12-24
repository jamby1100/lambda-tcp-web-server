#!/usr/bin/python3

from datetime import datetime
import json
from pprint import pprint
import socket
import os
from threading import Thread
import requests


class ThreadedServer(Thread):
    def __init__(self, host, port, tcp_server_base_url, timeout=60, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug
        self.tcp_server_base_url = tcp_server_base_url
        Thread.__init__(self)

        print("THREADED SERVER INIT")

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now())
            print('SERVER Starting...', '\n')

        self.listen()

    def listen(self):
        print("START LISTENING")
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))
        if self.debug:
            print(datetime.now())
            print('SERVER Socket Bound', self.host, self.port, '\n')

        # start listening for a client
        self.sock.listen(5)
        if self.debug:
            print(datetime.now())
            print('SERVER Listening...', '\n')
        
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # set a timeout
            client.settimeout(self.timeout)

            if self.debug:
                time_now = datetime.now()
                print(time_now)
                print('CLIENT Connected:', client, '\n')

            # start a thread to listen to the client
            Thread(target=self.listenToClient, args=(client, address, time_now)).start()

            # send the client a connection message
            # res = {
            #     'cmd': 'connected',
            # }
            # response = dumps(res)
            # client.send(response.encode('utf-8'))

    def listenToClient(self, client, address, time_now):
        # set a buffer size ( could be 2048 or 4096 / power of 2 )
        size = 1024
        while True:
            try:
                # try to receive data from the client
                data = client.recv(size).decode('utf-8')
                if data:
                    print(f"{time_now} AND THE DATA IS")
                    print(f"{time_now} {data}")

                    if data[0] != "<":
                        print("REMOVE FIRST")
                        data = data[1:]
                    
                        if data[0] != "<":
                            print("REMOVE SECOND")
                            data = data[1:]

                            if data[0] != "<":
                                print("REMOVE THIRD")
                                data = data[1:]


                    print(f"{time_now} AND THE REVISED DATA IS")
                    print(f"{time_now} {data}")

                    response = requests.post(
                        self.tcp_server_base_url,
                        data=data,
                        headers={"Content-Type":"application/xml"}
                    )


                    # data = json.loads(data.rstrip('\0'))
                    # if self.debug:
                    #     print(datetime.now())
                    #     print('CLIENT Data Received', client)
                    #     print('Data:')
                    #     pprint(data, width=1)
                    #     print('\n')

                    # send a response back to the client
                    res = {
                        'cmd': "Ready",
                        'data': "for the rock"
                    }

                    print(f"{time_now} AND THE RESPONSE IS")
                    print(f"{time_now} {response.text}")

                    response = response.text
                    client.send(response.encode('utf-8'))
                else:
                    raise Exception('Client disconnected')

            except Exception as error:
                print("AND THE ERROR IS: ")
                print(error)
                if self.debug:
                    print(datetime.now())
                    print('CLIENT Disconnected:', client, '\n')
                client.close()
                return False


if __name__ == "__main__":
    # ThreadedServer('0.0.0.0', 8108, timeout=86400, debug=True).start()

    print("BINDING!")

    bind_address = os.getenv("TCP_IP_ADDRESS_BIND")
    port = int(os.getenv("TCP_PORT_NUMBER"))
    tcp_server_base_url = os.getenv("APIGW_BASE_URL")
    timeout = int(os.getenv('TCP_SERVER_TIMEOUT'))
    ThreadedServer(bind_address, port, tcp_server_base_url, timeout=timeout, debug=True).start()

# TCP_IP_ADDRESS_BIND = 0.0.0.0
# TCP_PORT_NUMBER=9004
# APIGW_BASE_URL = https://6a