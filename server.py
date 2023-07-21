import json
import socket
from time import sleep
from threading import Thread
from traceback import print_exc

TPS = 1 / 20

def Get_IP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

class Server():
	def __init__(self):
		self.RUNNING = False

		self.clients = {}
		self.players = {}

	def Receive(self,address):
		self.players[address] = json.loads(self.clients[address].recv(1024).decode("utf-8"))

	def Send(self,address):
		data = [[port] + values for port,values in self.players.items() if port != address]

		self.clients[address].send(json.dumps(data).encode('utf-8'))

	def HandleClient(self,address):
		try:
			while self.RUNNING:
				self.Send(address)
			
				self.Receive(address)

				sleep(TPS)

			return 1

		except ConnectionResetError:
			print("Client Disconnected")

			self.clients.pop(address)
			self.players.pop(address)

			return 1
		
		except:
			print_exc()

			self.clients.pop(address)
			self.players.pop(address)

			return 0

	def AcceptClients(self,s):
		try:	
			while self.RUNNING:
				conn, addr = s.accept()

				print(f"Client Connected -> {addr[0]}:{addr[1]}")

				self.clients[str(addr[1])] = conn

				Thread(target=self.HandleClient,args=[str(addr[1])]).start()

		except OSError:
			pass
		except:
			print_exc()

	def Start(self,HOST: str, PORT: int):
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.bind((HOST, PORT))
				s.listen()

				self.RUNNING = True

				print("Server opened -> {}:{}".format(HOST,PORT))

				accept_thread = Thread(target = self.AcceptClients, args = [s])

				accept_thread.start()

				while True:
					sleep(TPS)
						
				s.close()

				self.RUNNING = False

				accept_thread.join()

		except OSError as err:
			if '10049' in str(err):
				print("Invalid Server Address -> {}:{}".format(HOST,PORT))
			elif '10048' in str(err):
				print("Server already open -> {}:{}".format(HOST,PORT))
			else:
				print_exc()
		except ConnectionResetError:
			print("Client Disconnected -> {}:{}".format(HOST,PORT))
		except json.decoder.JSONDecodeError:
			print("Invalid Data Received ")
			s.close()
		except:
			print_exc()


if __name__ == '__main__':
	server = Server()

	server.Start(Get_IP(),65432)