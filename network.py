import json
import socket
from time import sleep
from threading import Thread
from traceback import print_exc
from multiprocessing.pool import ThreadPool

TPS = 1 / 100

def FindServers(first=10, second=100):
	ip = Get_IP()
	base,middle,end = ip.split('.')[:-2], int(ip.split('.')[-2]), int(ip.split('.')[-1])

	possiblities = [".".join(base + [str(abs(middle + x))] + [str(abs(end + i))]) for x in range(-first,first) for i in range(-second, second) if middle + x > 0 and end + i > 0]
	
	threads = second * 2

	split_up = [possiblities[i * threads : i * threads + threads] for i in range(len(possiblities) // threads)]

	print(split_up)

	for s in split_up:
		with ThreadPool(processes = threads) as pool:
			a = [result for result in pool.map(CheckServer,s) if result["Response"]]

			print(a)

			if a == None: continue

			if len(a) > 0: return a

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
					"WorldSeed": int(data.split(":")[1]),
					"WorldSize": int(data.split(":")[2]),
					"WorldTicks": int(data.split(":")[3]),
				}

	except (ConnectionRefusedError, TimeoutError, socket.timeout):
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

		self.data = {}

	def Send(self,server):
		server.send(json.dumps(self.player.dump()).encode("utf-8"))

	def Receive(self,server):
		return json.loads(server.recv(1024).decode("utf-8"))

	def Loop(self,server):
		try:
			while self.CONNECTED:
				self.data = self.Receive(server)

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