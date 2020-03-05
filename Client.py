import socket
import sys
import os

class Client:
	sock = ""
	server_address = ""
	def connect(self):
		# Create TCP/IP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Connection the socket to the port Where the Server is listening
		server_address = ('localhost',5000)
		print("Conncting to Sever on port {0}".format(server_address[1]))
		sock.connect(server_address)
		return sock

	def openClient(self):
		try:
			while True:
				sock = Client.connect(self)
				#Recive The list of the files
				listOfFiles = sock.recv(1024)
				listOfFiles = Client.convert(self,listOfFiles.decode('utf-8'))
				#Display the Entry Message and Send The choosen answer to the server
				#Coloring The Message
				os.system('color 7')
				message = input("Please Choose Upload - Download - Exit"+"\n")
				sock.send(message.encode("utf-8"))
				os.system('cls')
				choice = Client.menu(self,message,sock,listOfFiles)
				os.system('cls')
				if choice == "break":
					break
		finally:
			sock.close()

	#Menu Screen
	def menu(self,message,sock,listOfFiles):
		#check The enter Message

		#Upload
		if message == 'upload' or message == 'Upload' or message == 'u':
			Client.upload(self,sock)
				
		#Download
		elif message == 'download' or message == 'Download' or message == 'd':
			Client.download(self,sock,listOfFiles)

		#Exit
		elif message == 'Exit' or message == 'exit' or message == 'e':
			print("Exit")
			return "break"
				
		#Worng Choice
		else:
			print("Please Enter Valid Choice")

	
	#Method Of Upload
	def upload(self,sock):
		print(Client.allFiles(self))
		fileName = input("Please Choose a File From The Above"+"\n")
		if (fileName in Client.allFiles(self)):
			sock.send(fileName.encode('utf-8'))
			f = open(fileName,"rb")
			print("Uploading to The Server")
			load = f.read(1024)
			while (load):
				sock.send(load)
				load = f.read(1024)
			print("Uploaded Sucessfully")
			f.close()
		else:
			print("No File With This Name")
			input("Please Press Enter and Try Again")
			os.system('cls')
			Client.upload(self,sock)
		input("Please Press Enter To Return To The Main Menu")


	#Method Of Download
	def download(self,sock,listOfFiles):
		print(listOfFiles)
		fileName = input("Please Enter The File Name As the Above "+"\n")
		if(fileName in listOfFiles):
			sock.send(fileName.encode('utf-8'))
			f = open(fileName,"wb")
			print("Reciving the File")
			loading = sock.recv(1024)
			while (loading):
				f.write(loading)
				loading = sock.recv(1024)
			print("Finished All Data")
			f.close()
			input("Please Press Enter To Return To The Main Menu")
		else:
			input("No File With This Name\n,Press Enter Please")
			Client.download(self,sock,listOfFiles)

	#Method Of lising all files
	def allFiles(self):
		allfilesName = []
		allfilesName = os.listdir("./")
		return allfilesName

	#Method Converts String Into List
	def convert(self,listOfFile):
		listOfFile = listOfFile.replace("'",'')
		listOfFile = listOfFile.replace("[",'')
		listOfFile = listOfFile.replace("]",'')
		listOfFile = listOfFile.replace(" ",'')
		return listOfFile.split(',')

c = Client()
c.openClient()
