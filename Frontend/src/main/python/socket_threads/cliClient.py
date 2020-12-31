import socket
import threading
import sys
import os
from io import StringIO

HEADER = 128
PORT = 5005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '127.0.1.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start(handle):
	client.connect(ADDR)
	send(handle)
	while True:
		thread = threading.Thread(target=receiver)
		thread.daemon = True
		thread.start()

		to_send = input()
		if to_send == 'd':
			send(DISCONNECT_MESSAGE)
#			client.shutdown(socket.SHUT_RDWR)
			client.close()
			break

		send(to_send)


def receiver():
	while True:
		inc_msg = client.recv(HEADER).decode(FORMAT)
		print(inc_msg)


def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)


if __name__ == '__main__':
	try:
		handle = input("Enter handle: ")
		print("[CONNECTING] Connecting to Server...")
		start(handle)
	except KeyboardInterrupt:
		print('n/Disconnected')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
