import socket
import time

import requests

from API.config import config

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        logging.info(f"REQUEST SENT :: {request}")
        time.sleep(0.200)
        self.sock.sendall(request.encode('utf-8'))

    def receiveResponseFromSocket(self):
        buf = bytearray()
        while True:
            chunk = self.sock.recv(12288)
            if not chunk:
                break
            buf.extend(chunk)
            logging.info(f"RESPONSE RECEIVED :: {buf.decode('utf-8')}")
            time.sleep(0.200)
            return buf.decode('utf-8')


    def httpsRequest(self, url, request, requestFormat):
        logging.info(f"REQUEST SENT :: {request}")
        time.sleep(0.200)
        headers = {"Content-Type": f"application/json"}
        self.httpsResponse  = requests.post(url, json=request, verify=False, headers=headers).text

    def receiveResponsehttps(self):
        logging.info(f"RESPONSE RECEIVED :: {self.httpsResponse}")
        time.sleep(0.200)
        return self.httpsResponse

    def closeSocket(self): self.sock.close()