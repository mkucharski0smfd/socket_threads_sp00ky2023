import socket
import threading
import sys
import os

HEADER = 128
PORT = 5005
SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
IDENTIFIER = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# to replace later with database
msg_list = []
clients = []


class threadTerminator:
	def __init__(self):
		self._running = True


	def terminate(self):
		self._running = False


	def get_handle(self, conn, addr):
		handle_length = conn.recv(HEADER).decode(FORMAT)
		if handle_length:
			handle_length = int(handle_length)
			handle = conn.recv(handle_length).decode(FORMAT)
			print(handle + ' joined the server')
			self.welcome_announce(handle)

		self.handle_client(conn, addr, handle)
  
	def welcome_announce(self, handle):
		for client in clients:
			client.sendall(f'[{handle}] has joined the channel'.encode(FORMAT))
	


	#def tic_toc(self)

	def handle_client(self, conn, addr, handle):
		connected = True
		while connected:
			msg_length = conn.recv(HEADER).decode(FORMAT)
			if msg_length:
				msg_length = int(msg_length)
				msg = conn.recv(msg_length).decode(FORMAT)
				if msg == DISCONNECT_MESSAGE:
					connected = False
					print(f"[{handle}] {msg}")
					clients.remove(conn)
					print([clients])
					break

				if msg != DISCONNECT_MESSAGE or msg != handle:
					msg_list.append(msg)
					print(msg_list)

					self.updater(conn, addr, handle)

		self.terminate()


	def updater(self, conn, addr, handle):
		other_msg = msg_list[-1]
		other_msg = ''.join([str(elem) for elem in other_msg])

		for client in clients:
			client.sendall(f'[{handle}]: {other_msg}'.encode(FORMAT))


def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}, Port: {PORT}")
	while True:
		conn, addr = server.accept()
		clients.append(conn)
		print([clients])
		c = threadTerminator()
		# timed_message = threading.Thread(target=c.tic_toc, args=())
		thread = threading.Thread(target=c.get_handle, args=(conn, addr))
		thread.start()		
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



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