import socket
import threading
import sys
import os

HEADER = 128
PORT = 5003
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
IDENTIFIER = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# to replace later with database
old_msg_list = []
msg_list = ['']
clients = []


def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}, Port: {PORT}")
	while True:
		conn, addr = server.accept()
		clients.append(conn)
		thread = threading.Thread(target=get_handle, args=(conn, addr))
		thread.start()		
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def get_handle(conn, addr):
	handle_length = conn.recv(HEADER).decode(FORMAT)
	if handle_length:
		handle_length = int(handle_length)
		handle = conn.recv(handle_length).decode(FORMAT)
		print(f"[NEW CONNECTION] {handle} connected")

	handle_client(conn, addr, handle)


def handle_client(conn, addr, handle):
	connected = True
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False

			print(f"[{handle}] {msg}")

			if msg != DISCONNECT_MESSAGE or msg != handle:
				old_msg_list = msg_list
				msg_list.append(msg)
				print(msg_list)
#call updater to send the message to the other clients
				updater(conn, addr, handle)
	conn.close()


def updater(conn, addr, handle):
	other_msg = msg_list[-1]
	other_msg = ''.join([str(elem) for elem in other_msg])

	if old_msg_list != msg_list:
		for client in clients:
			client.send(f'[{handle}]: {other_msg}'.encode(FORMAT), )
#			client.send(('[{}]: {}'.format(handle, other_msg)).encode(FORMAT))


if __name__ == '__main__':
	try:
		print("[STARTING] Server is starting...")
		start()
	except KeyboardInterrupt:
		print("[SHUTDOWN] Shutting Down Server...")
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)