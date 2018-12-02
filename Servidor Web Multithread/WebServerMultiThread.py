import socket, sys
import _thread

MAX_CONNECTIONS = 5
BUFFER_SIZE = 8192

def startServer():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', LISTENING_PORT))
        server.listen(MAX_CONNECTIONS)
        print("Iniciando Sockets...")
        print("Sockets iniciados com sucesso...")
        print("Servidor iniciado com sucesso - %d\n" % (LISTENING_PORT))
    except Exception:
        print("Nao foi possivel inicializar os Sockets")
        sys.exit(2)
    
    while 1:
        try:
            connection, address = server.accept()
            _thread.start_new_thread(httpRequest, (connection, address))
        except KeyboardInterrupt:
            server.close()
            print("\nDesligando servidor HTTP MultiThread...")
            sys.exit(1)
    
    server.close()

def httpRequest(connection, address):
    try:
        data = connection.recv(BUFFER_SIZE)
        filename = data.split()[1]
        file = open(filename[1:])
        fileData = file.read()
        connection.send(str.encode("HTTP/1.0 200 OK\r\n\r\n"))
        for i in range(0, len(fileData)):  
            connection.send(str.encode(fileData[i]))
        
        connection.send(str.encode("\r\n"))
    except IOError:
	    connection.send(str.encode("HTTP/1.0 404 Not Found\r\n\r\n"))
	    connection.send(str.encode("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"))

    connection.close()

if __name__ == '__main__':
    try:
        LISTENING_PORT = int(input("Porta para iniciar o sevidor HTTP: "))
    except KeyboardInterrupt:
        print("Finalizando aplicacao...")
        sys.exit()

    startServer()