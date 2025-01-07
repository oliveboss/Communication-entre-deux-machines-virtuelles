import socket
import hashlib
import random
import time

SERVER_ADDRESS = ('127.0.0.1', 21222) #Adresse et port du serveur 
BUFFER_SIZE = 1024 # taille de morceau de fichier 
reliability = 1  # Taux de fiabilité du réseau (par exemple)
TIMEOUT = 3  # Temps d'attente pour l'accusé de réception en secondes
MAX_RETRIES = 5  # Nombre maximal de tentatives d'envoi


# Fonction pour calculer l'empreinte de hachage MD5 d'un fichier
def calculate_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(BUFFER_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

# Fonction pour poignée de main 
def handshake(server_socket, client_address):
    server_socket.sendto(b'SYN-ACK', client_address) # envoi de syn
    data, _ = server_socket.recvfrom(BUFFER_SIZE) # Reception si cest un ACk connexion réuissi
    if data.decode() == 'ACK':
        print("Poignée de main avec le client réussie.")

# Fonction pour envoyer le fichier 
def send_file(server_socket, file_path, max_chunk_size, client_address, reliability):
    with open(file_path, 'rb') as file:   # on ouvre le fichier en binaire 
        chunk_counter = 0 # initialisation de morceau de fichier 
        while True:
            chunk = file.read(max_chunk_size)
            if not chunk:   # si on ne trouve plus de morceau la transmission est terminé
                server_socket.sendto(b'Fin de transmission', client_address)
                print("Tous les morceaux de fichiers ont été envoyés. Envoi du message de clôture.")
                break
            if random.random() < reliability: # pour la simulation d'erreur un nombre aléatoire est utilisé
                server_socket.sendto(chunk, client_address)
                print(f"Envoyé {len(chunk)} octets au client {client_address}")
                chunk_counter += 1  #Incrémentation du nbr de morceau a chaque envoi 
                if chunk_counter % 5 == 0:
                    # Attendre l'ACK du client après chaque 5 blocs
                    ack_received = False
                    retries = 0
                    while not ack_received and retries < MAX_RETRIES:
                        try:
                            server_socket.settimeout(TIMEOUT)  # Timeout pour l'accusé de réception
                            data, _ = server_socket.recvfrom(BUFFER_SIZE)
                            if data == b'ACK':
                                ack_received = True
                                print("ACK reçu du client.")
                        except socket.timeout:
                            print("Timeout : retransmission du morceau de données.")
                            server_socket.sendto(chunk, client_address)
                            retries += 1
                    if retries == MAX_RETRIES:
                        print("Échec : aucune réponse après 5 tentatives.")
                        break
            else:
                print("Erreur de transmission simulée. Le message n'a pas été envoyé.")

def main():
      # Création d'une socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(SERVER_ADDRESS)  #liaison a l,adresse du serveur 
   
     # Demarrage du serveur 
    print("Le serveur UDP est démarré. En attente de connexions...")
      
      #Reception de syn du client (poigné de main )
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    if data.decode() == 'SYN':
        print(f"SYN reçu du client {client_address}. Initiating handshake...")
        handshake(server_socket, client_address)

        # Reception des parametres 
        params, _ = server_socket.recvfrom(BUFFER_SIZE)
        max_chunk_size, _ = map(int, params.decode().split(','))
       
        #Envoi de confirmation de parametre au client
        server_socket.sendto(b'Params confirmes', client_address)
        print("Confirmation des paramètres envoyée au client.")
      
        #Envoi de fichiers au client 
        file_path =  "C:\\Users\\amouz\\OneDrive\\Bureau\\INF26207_TP02_H2024_AMOUZOU_et_ABENI\\INF26207_TP01_H2024_AMOUZOU_et_ABENI.docx"
        send_file(server_socket, file_path, max_chunk_size, client_address, reliability)

        # Calcul de l'empreinte du fichier original
        original_hash = calculate_hash(file_path)

        # Envoi de l'empreinte au client
        server_socket.sendto(original_hash.encode(), client_address)
        print("Empreinte du fichier envoyée au client.")

    server_socket.close()

if __name__ == "__main__":
    main()
