import socket, sys
import _thread

MAX_CONNECTIONS = 5
BUFFER_SIZE = 8192

def start():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', LISTENING_PORT))
        server.listen(MAX_CONNECTIONS)
        print("Iniciando Sockets...")
        print("Sockets iniciados com sucesso...")
        print("Servidor iniciado com sucesso - %d\n" % (LISTENING_PORT))
    except Exception:
        print("Não foi possivel inicializar os Sockets")
        sys.exit(2)
    
    while 1:
        try:
            connection, address = server.accept()
            _thread.start_new_thread(proxyClient, (connection, address))
        except KeyboardInterrupt:
            server.close()
            print("\nDesligando servidor Proxy...")
            sys.exit(1)
    
    server.close()

def proxyClient(connection, address):
    try:
        data = connection.recv(BUFFER_SIZE)
        url = data.split()[1].decode()
        httpPos = url.find("://")
        if(httpPos == -1):
            temp = url
        else:
            temp = url[(httpPos+3):]
        
        portPos = temp.find(":")
        webserverPos = temp.find("/")
        if webserverPos == -1:
            webserverPos = len(temp)
        webserver = ""
        port = -1
        if(portPos == -1 or webserverPos < portPos):
            port = 80
            webserver = temp[:webserverPos]
        else:
            port = int((temp[(portPos+1):])[:webserverPos-portPos-1])
            webserver = temp[:portPos]
        
        proxyServer(webserver, port, connection, address, data)
    except Exception:
        pass

def proxyServer(webserver, port, connection, address, data):
    try:
        requisitionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        requisitionSocket.connect((webserver, port))
        requisitionSocket.sendall(data)
        while 1:
            requestResponse = requisitionSocket.recv(BUFFER_SIZE)
            if(len(requestResponse) > 0):
                connection.send(requestResponse)
                responseSize = float(len(requestResponse))
                responseSize = float(responseSize / 1024)
                responseSize = "%.3s" % (str(responseSize))
                responseSize = "%s KB" % (responseSize)
                print("Requisicao completa: %s => %s <= " % (str(address[0]), str(responseSize)))
            else:
                break
        
        requisitionSocket.close()
        connection.close()
    except socket.error:
        requisitionSocket.close()
        connection.close()
        sys.exit(1)

if __name__ == '__main__':
    try:
        LISTENING_PORT = int(input("Porta para iniciar o sevidor Proxy: "))
    except KeyboardInterrupt:
        print("Finalizando aplicacao...")
        sys.exit()

    start()