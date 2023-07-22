import json
import socket
from time import sleep
from threading import Thread
from traceback import print_exc
from multiprocessing.pool import ThreadPool

TPS = 1 / 60

def FindServers(search_range=10):
	ip = Get_IP()
	base,end = ip.split('.')[:-1], int(ip.split('.')[-1])

	possiblities = [".".join(base + [str(abs(end + i))]) for i in range(-search_range, search_range)]
	
	with ThreadPool(processes = 25) as pool:
		return [result for result in pool.map(CheckServer,possiblities) if result["Response"]]

def CheckServer(host):
	HOST, PORT = host, 65432

	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(1.0)

			s.connect((HOST, PORT))

			s.send(b"get")

			data = s.recv(1024).decode("utf-8").lower()

			if "valid" in data:
				return {
					"Response": 1,
					"Address": HOST,
					"Seed": int(data.split(":")[1]),
					"Ticks": int(data.split(":")[2]),
				}

	except ConnectionRefusedError:
		pass
	except TimeoutError:
		pass
	except:
		print_exc()

	return {
		"Response": 0
	}

def Get_IP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

class Client():
	def __init__(self,player):
		self.CONNECTED = False

		self.player = player

		self.data = []

	def Send(self,server):
		server.send(json.dumps(self.player.dump()).encode("utf-8"))

	def Receive(self,server):
		return json.loads(server.recv(1024).decode("utf-8"))

	def Loop(self,server):
		try:
			while self.CONNECTED:
				self.data = self.Receive(server)

				print(self.data)

				self.Send(server)

				sleep(TPS)

			return 1
		except ConnectionResetError:
			print("Server Closed")

			return 1

		except:
			print_exc()

			return 0

	def Connect(self, HOST: str, PORT: int):
		t = Thread(target=self.main,args=[HOST,PORT])
		t.daemon = True
		t.start()

	def main(self,HOST,PORT):
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((HOST, PORT))
				s.send(b"join")

				print("Connecting -> {}:{}".format(HOST,PORT))

				self.CONNECTED = True

				self.Loop(s)

				self.CONNECTED = False

		except ConnectionRefusedError:
			print("Server not open -> {}:{}".format(HOST,PORT))
		except (ConnectionAbortedError,ConnectionResetError):
			print("Server Closed -> {}:{}".format(HOST,PORT))
		except:
			print_exc()

		self.CONNECTED = False