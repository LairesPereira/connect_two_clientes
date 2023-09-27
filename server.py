import socket
import threading

print(socket.gethostname())

HEADER = 64
FORMAT = 'utf-8'
DISCONECT = '_disconect_now'
PORT = 5050 # Setar uma porta que esteja livre para a comunicação

# Endereço local na rede pode ser setado manualmente
# SERVER = '172.16.63.147' 

# Pegar o nome do computador localmente na rede e encontrar o endereço IP por este nome
SERVER = socket.gethostbyname('localhost')
# SERVER = '172.16.63.147'

ADDR = (SERVER, PORT)

# Primeiro arg diz ao socket que tipo de endereços vamos trabalhar
# Segundo arg diz ao socket que estamos transferindo dados por "STREAM"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

def handle_client(conn, addr):

    print(f'[NOVA CONEXÃO]: {addr} conectado!')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if(msg_length):
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if(msg == DISCONECT):
                connected = False

            print(f'[{addr}]: {msg}')
            conn.send('Mensagem recevida'.encode(FORMAT))
        
    conn.close()
    
# Permitir o servidor iniciar novas conexoes e passalas para handle_cliente que
# irá rodar essas conexoes em uma nova thread
def start():
    server.listen()
    print(f'[LISTENING]: Server is listening on {SERVER}')

    while True:
        # Aguardamos uma nova conexão e armazenamos o endereço em addr
        # para sabermos para onde enviar informacoes de volta atraves do objeto conn
        conn, addr = server.accept() 

        # Criamos uma nova thread para cada conexao passando 
        # a funcao que irá lidar com o cliente
        # e também o endereço obtido na conexão
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        print(f'[CONEXOES ATIVAS]: {threading.active_count() - 1}')


print('[INICIANDO]: O servidor está iniciando...')
start()




