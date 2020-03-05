import socket
import sys
import os

class Server:

	#The Method That Get All Files Beside the Server
	def getTheListOfFiles():
		listOfFiles = []
		listOfFiles = os.listdir("./")
		return listOfFiles


	def CreateSocket(self):
		#Define the ip address and the socket
		server_address = ('localhost',5000)
		#Create a TCP/IP Socket 
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#Bind the Socket to the Port
		sock.bind(server_address)
		#listen For The Client
		sock.listen(1)
		while True:
			#Wait for a connection
			print("Waiting For a connection")
			connection, client_address = sock.accept()
			print("There is a client with ip {0}".format(client_address[0]))
			#Send All Files To The Client
			allFiles = Server.getTheListOfFiles()
			connection.send(str(allFiles).encode('utf-8'))
			try:
				clientRequest = connection.recv(1024)
				requestString = clientRequest.decode("utf-8")
				if requestString == 'download' or requestString == 'd':
					Server.downLoad(connection)

				elif requestString == 'upload' or requestString == 'u':
					Server.upLoad(connection)
			finally:
				connection.close()
				os.system('cls')

	def downLoad(connection):
		clientRequest = connection.recv(1024)
		fileRequest = clientRequest.decode("utf-8")
		f = open(fileRequest,"rb")
		print ("Sending to The Client")
		load = f.read(1024)
		while load:
			connection.send(load)
			load = f.read(1024)
		f.close()
		print("Finished All Data")

	def upLoad(connection):
		clientRequest = connection.recv(1024)
		fileName = clientRequest.decode("utf-8")
		print("Recieved Upload")
		with open(fileName, 'wb') as f:
			print('file incoming...')
			while True:
				data = connection.recv(1024)
				if not data:
					break
				f.write(data)
		print(fileName + " has been Received!")
				
myclass = Server()
myclass.CreateSocket() 