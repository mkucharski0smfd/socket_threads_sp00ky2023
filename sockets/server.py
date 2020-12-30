import socket
import threading

HEADER = 64
PORT = 5005
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


# gets the users handle and then listens for messages
def get_handle(conn, addr):
	handle_length = conn.recv(HEADER).decode(FORMAT)
	if handle_length:
		handle_length = int(handle_length)
		handle = conn.recv(handle_length).decode(FORMAT)
		print(f"[NEW CONNECTION] {handle} connected")
#		x = True
#		break

	handle_client(conn, addr, handle)

# handles all messages received from the client(s)
# also adds all messages to the database/list
def handle_client(conn, addr, handle):
	connected = True
	while connected:
#		thread1 = threading.Thread(target=updater, args=(conn, addr, handle))
#		thread1.start()

		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False

			print(f"[{handle}] {msg}")

			if msg != DISCONNECT_MESSAGE and msg != handle:
				old_msg_list = msg_list
				msg_list.append(msg)
#				print(msg_list)
#				call updater to send the message to the other clients. may need thread!
				updater(conn, addr, handle)
	conn.close()

# handles sending messages from one client to the others
# client only receives their own messages in bytes
def updater(conn, addr, handle):
	other_msg = msg_list[-1]
	other_msg = ''.join([str(elem) for elem in other_msg])

	if old_msg_list != msg_list:
#		conn.send(f'[{handle}]: {other_msg}'.encode(FORMAT))
		for client in clients:
#			client.send(f'[{handle}]: {other_msg}'.encode(FORMAT), )		
			message = other_msg.encode(FORMAT)
			msg_length = len(message)
			send_length = str(msg_length).encode(FORMAT)
			send_length += b' ' * (HEADER - len(send_length))
			conn.send(send_length)
			conn.send(message)		

# starts the server and threads out the message input, as well as the updater to
# their own threads.
def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}, Port: {PORT}")
	while True:
		conn, addr = server.accept()
		clients.append(conn)
		thread = threading.Thread(target=get_handle, args=(conn, addr))
		thread.start()		
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Server is starting...")
start()
