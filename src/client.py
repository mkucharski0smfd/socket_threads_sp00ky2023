import socket
import threading

HEADER = 64
PORT = 5005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '127.0.1.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)


# client only receives what they send, need to fix
def receiver():
	while True:
#		print(client.recv(2048))

		msg_length = client.recv(2048).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = client.recv(msg_length).decode(FORMAT)
		print(msg)

def start(handle):
	client.connect(ADDR)
	send(handle)
	while True:
		thread = threading.Thread(target=receiver)
#		thread.start()
		to_send = input('[MY MESSAGE]: ')
		if to_send == 'd':
			send(DISCONNECT_MESSAGE)
			client.close()
			quit()
			break
		send(to_send)

print("[CONNECTING] Connecting to Server...")
handle = input("Enter handle: ")
start(handle)
