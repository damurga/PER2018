import socket
import os

IP = "212.128.255.160"
PORT = 9031
MAX_OPEN_REQUESTS = 6

def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024).decode("utf-8")
    b = str(mensaje_solicitud).split(" ")
    a = b[1].replace("/", "")
    print (mensaje_solicitud)
    if os.path.exists(a + ".html"):
        FILE_HTML = a + ".html"
    elif a == "index.html" or a == "":
        FILE_HTML = "green.html"
    else:
        FILE_HTML = "error.html"

    with open(FILE_HTML, "r") as f:
        contenido = f.read()

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))


    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:

    serversocket.bind((IP, PORT))


    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:

        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()


        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)
        clientsocket.close()

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")
