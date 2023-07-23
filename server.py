import json
import math
import socket
import random
from time import sleep,time
from threading import Thread
from traceback import print_exc

TPS = 1 / 100

def Get_IP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

def Distance(point1,point2):
	return math.sqrt( pow(point2[0]-point1[0],2) + pow(point2[1]-point1[1],2) )

class Server():
	def __init__(self, seed = random.randint(100000000,999999999), map_size = 5000):
		self.RUNNING = False

		self.clients = {}
		self.players = {}
		self.locations = {}

		self.seed = seed
		self.map_size = map_size

		self.ticks_alive = 0

		print("World Seed:",self.seed)

	def Receive(self,address):
		self.players[address] = json.loads(self.clients[address].recv(1024).decode("utf-8"))

	def Send(self,address):
		data = [{"Port": port, "Spawnpoint": self.locations[port]} | values for port,values in self.players.items() if port != address]

		self.clients[address].send(json.dumps({"Tick": self.ticks_alive, "Players": data, "Spawnpoint": self.locations[address]}).encode('utf-8'))

	def CheckClient(self,conn,addr):
		try:
			data = conn.recv(1024).decode('utf-8').lower()

			if data == "get":
				conn.send(f"valid:{self.seed}:{self.map_size}:{self.ticks_alive}".encode("utf-8"))
				conn.close()

			elif data == "join":
				print(f"[{self.ticks_alive}] Client Connected -> {addr[1]}")

				self.clients[str(addr[1])] = conn

				self.CreatePlayer(str(addr[1]))

				self.HandleClient(str(addr[1]))

		except OSError:
			pass
		except:
			print_exc()

	def CreatePlayer(self,address):
		border = int(self.map_size * 0.8)

		while True:
			position = [random.randint(-border,border),random.randint(-border,border)]

			for player,location in self.locations.items():
				if Distance(position,location) < 500:
					break
			else:
				break

		self.locations[address] = position

	def HandleClient(self,address):
		try:
			while self.RUNNING:
				a = time()

				self.Send(address)
			
				self.Receive(address)

				sleep(max(0,TPS - (time() - a)))

			return 1

		except ConnectionResetError:
			print(f"[{self.ticks_alive}] Client Disconnected -> {address}")

			self.clients.pop(address)
			self.players.pop(address)
			self.locations.pop(address)

			return 1
		
		except:
			print_exc()

			self.clients.pop(address)
			self.players.pop(address)
			self.locations.pop(address)

			return 0

	def AcceptClients(self,s):
		try:	
			while self.RUNNING:
				conn, addr = s.accept()

				Thread(target=self.CheckClient,args=[conn,addr]).start()

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

				accept_thread.daemon = True

				accept_thread.start()

				while True:
					sleep(TPS)

					self.ticks_alive += 1
						
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