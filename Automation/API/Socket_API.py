import socket
import time

import requests

from API.config import config


class Adsdk_Socket:

    def __init__(self):
        self.sock = None
        self.comm = config.commProtocol()
        self.ip = config.Config_machine_ip()
        self.response = None
        self.httpsResponse = None

    def openSocket(self, port):
        server_address = (self.ip, int(port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_address)

    def sendRequest(self, request):
        print(f"Request send :: {request}")
        time.sleep(0.500)
        self.sock.sendall(request.encode('utf-8'))

    def receiveResponseFromSocket(self):
        buf = bytearray()
        while True:
            chunk = self.sock.recv(12288)
            if not chunk:
                break
            buf.extend(chunk)
            print(f"Response Rec :: {buf.decode('utf-8')}")
            return buf.decode('utf-8')

    def httpsRequest(self, url, request, requestFormat):
        print(f"Request send :: {request}")
        time.sleep(0.500)
        headers = {"Content-Type": f"application/json"}
        self.httpsResponse  = requests.post(url, json=request, verify=False, headers=headers).text

    def receiveResponsehttps(self):
        print(f"Response Rec :: {self.httpsResponse}")
        return self.httpsResponse

    def closeSocket(self): self.sock.close()