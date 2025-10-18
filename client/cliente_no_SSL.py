import socket
import sys, errno

import hashlib, hmac

import uuid

HOST = 'localhost'
PORT_HOST = 8000

with open("../secrets/key.txt", "r") as file:
        KEY = file.read()

# Crear  el socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


with client_socket as s:
    s.connect((HOST, PORT_HOST))
    while True:
        data = s.recv(1024)
        if data:
            #print('Received', data.decode())
            #print(data.decode())
            data_splitted = data.decode().split(';')
            mode = data_splitted[0]
            message = data_splitted[1]
            #print(mode, message)
            print(message)
            if mode == 'inp':
                message_sent = input()
                while message_sent == "":
                    message_sent = input()
                s.sendall(message_sent.encode())
            elif mode=="msg":
                nonce = uuid.uuid4().hex
                #print('Received', data.decode())
                #print(data.decode())
                dest = input("Destinatario: \n")
                ms = input("Mensaje: \n")
                mac_client = hmac.new(KEY.encode(), dest.encode()+b","+ms.encode()+str(nonce).encode(), hashlib.sha256).digest()
                msg = f"{dest},{ms},{mac_client.hex()},{nonce}"
                try:
                    s.sendall(msg.encode())
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass
            elif mode=="dest":
                dest = input("Destinatario: \n")
                try:
                    s.sendall(dest.encode())
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass
            
            elif mode=="mss":
                ms = input("Mensaje: \n")
                mac_client = hmac.new(KEY.encode(), dest.encode()+b","+ms.encode(), hashlib.sha256).digest()
                print(ms,mac_client)
                msg = f"{ms};{mac_client.hex()}"
                try:
                    s.sendall(msg.encode())
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass
            # elif mode == "info":
            #     print("ke")
            #     message_sent = ""
            #     s.sendall(message_sent.encode())
        else:
            break
