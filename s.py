import socket
import threading

def handle_client(connfd,filepath):
	command = connfd.recv(1024).decode('utf-8')

	print(f"Recieved command : {command}")
	connfd.send(b"ok")
	if command == "send":
		print("Going to recieve file from client")
		reciever(connfd,"Client_data")
	elif command == "recieve":
		sender(connfd,filepath)
	else:
		print("Unknown command")
	connfd.close()
def sender(connfd,filepath):
   # ext = filepath[filepath.find('.'):]
    #print(ext)
    filename = filepath.removeprefix("/home/s2022103046/")
    connfd.send(filename.encode())
    ack = connfd.recv(1024).decode('utf-8')
    with open (filepath,"rb") as fileptr:
        file_data = fileptr.read(1024)

        while file_data:
            connfd.send(file_data)
            file_data = fileptr.read(1024)
    print(f"File sent : {filepath}")
def reciever(connfd,savepath):
	connfd.send(b"ok")
	#ext = connfd.recv(1024).decode('utf-8')
	filename = connfd.recv(1024).decode('utf-8')

	#filename = savepath+ext
	with open(filename,"wb") as fileptr:
		file_data = connfd.recv(1024)
		while file_data:
			fileptr.write(file_data)
			file_data = connfd.recv(1024)
	print(f"File recieved and saved to {filename}")

def start_server(host,port,filepath):
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockfd.bind((host,port))
    sockfd.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        connfd,cliaddr = sockfd.accept()
        print(f"Connection from the client : {cliaddr}")
        cli_handler = threading.Thread(target=handle_client,args=(connfd,filepath))
        cli_handler.start()

if __name__ == "__main__":
    filepath = input("Enter the file to send : ")
    host = "10.5.12.254"
    port = 53046
    start_server(host,port,filepath)
