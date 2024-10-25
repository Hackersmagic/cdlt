import socket

def send_file(ip,port,file_path):
	sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sockfd.connect((ip,port))
	
	sockfd.send("send".encode())
	ack = sockfd.recv(1024).decode('utf-8')
	if(ack == "ok"):
		with open(file_path,"rb") as fileptr:
			file_data = fileptr.read(1024)
			while file_data:
				sockfd.send(file_data)
				file_data = fileptr.read(1024)
	print(f"File sent : {file_path}")
	sockfd.close()
def recieve_file(ip,port,savepath):
	sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sockfd.connect((ip,port))


	sockfd.send("recieve".encode())
	ack = sockfd.recv(1024).decode('utf-8')
	if(ack == "ok"):
		with open(savepath,"wb") as fileptr:
			file_data = sockfd.recv(1024)
			while file_data:
				fileptr.write(file_data)
				file_data = sockfd.recv(1024)
	print(f"File recieved and saved as {savepath}")
	sockfd.close()

if __name__ == "__main__":
	ip = "10.5.12.254"
	port = 53036
	savepath = "recievedfile.txt"
	choice = input("(send) or (recieve) : ")
	#temp = choice.lower()
	print("your choice : ",choice)
	if choice.lower() == "send":
		file_path = input("Enter the filepath : ")
		send_file(ip,port,file_path)
	elif choice.lower() == "recieve":
		save_path = input("Enter the name with extension the file to be saved : ")
		recieve_file(ip,port,save_path)
	else:
		print("Invalid choice")
