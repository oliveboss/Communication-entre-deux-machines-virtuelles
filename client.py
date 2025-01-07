import socket  # Module permettant la communication réseau
import hashlib  # Module pour calculer les empreintes de hachage
import random  # Module pour générer des nombres aléatoires
import time  # Module pour la gestion du temps

# Adresse IP et port du serveur
SERVER_ADDRESS = ('127.0.0.1', 21222)
# Taille du tampon pour recevoir les données
BUFFER_SIZE = 1024
# Taux de fiabilité du réseau (par exemple)
reliability = 0.95  
# Temps d'attente pour l'accusé de réception en secondes
TIMEOUT = 3  
# Nombre maximal de tentatives d'envoi
MAX_RETRIES = 5  

# Fonction pour calculer l'empreinte de hachage MD5 d'un fichier
def calculate_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(BUFFER_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

# Fonction pour initier la poignée de main avec le serveur
def handshake(client_socket):
    # Envoi du signal de synchronisation (SYN) au serveur
    client_socket.sendto(b'SYN', SERVER_ADDRESS)
    # Réception de la réponse du serveur
    data, _ = client_socket.recvfrom(BUFFER_SIZE)
    # Vérification de la réponse du serveur
    if data.decode() == 'SYN-ACK':
        # Envoi de l'accusé de réception (ACK) au serveur
        client_socket.sendto(b'ACK', SERVER_ADDRESS)
        print("Poignée de main avec le serveur réussie.")

# Fonction pour recevoir le fichier envoyé par le serveur
def receive_file(client_socket, file_path, max_chunk_size, reliability, max_chunks_before_ack):
    with open(file_path, 'wb') as file:
        chunks_received = 0
        while True:
            # Réception d'un morceau de fichier
            chunk, _ = client_socket.recvfrom(BUFFER_SIZE)
            # Vérification de la fin de transmission
            if chunk == b'Fin de transmission':
                print("Transmission terminée.")
                break
            # Simulation d'une erreur de transmission en ignorant le message avec une certaine probabilité
            if random.random() > reliability:
                print("Erreur de transmission : message ignoré.")
            else:
                # Écriture du morceau de fichier dans le fichier local
                file.write(chunk)
                chunks_received += 1
                print(f"Morceau de données {chunks_received} bien reçu.")
                # Envoi d'un accusé de réception (ACK) au serveur après chaque N morceaux de fichier
                if chunks_received % max_chunks_before_ack == 0:
                    client_socket.sendto(b'ACK', SERVER_ADDRESS)

# Fonction principale
def main():
    # Création d'une socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Initialisation de la connexion avec le serveur
    handshake(client_socket)

    # Paramètres pour la réception du fichier
    max_chunk_size = 1024
    max_chunks_before_ack = 5
    params = f"{max_chunk_size},{max_chunks_before_ack}"
    # Envoi des paramètres au serveur
    client_socket.sendto(params.encode(), SERVER_ADDRESS)

    # Réception de la confirmation des paramètres du serveur
    data, _ = client_socket.recvfrom(BUFFER_SIZE)
    if data.decode() == 'Params confirmes':
        print("Paramètres confirmés par le serveur.")

        # Chemin du fichier à recevoir
        file_path = "received_file.docx"
        # Réception du fichier envoyé par le serveur
        receive_file(client_socket, file_path, max_chunk_size, reliability, max_chunks_before_ack)

        # Réception de l'empreinte du fichier envoyée par le serveur
        received_hash, _ = client_socket.recvfrom(BUFFER_SIZE)

        # Calcul de l'empreinte du fichier reçu
        received_hash_local = calculate_hash(file_path)

        # Comparaison des empreintes pour vérifier l'intégrité du fichier
        if received_hash.decode() == received_hash_local:
            print("Les empreintes des fichiers correspondent. Le fichier reçu est identique au fichier envoyé.")
        else:
            print("Les empreintes des fichiers ne correspondent pas. Le fichier reçu est différent du fichier envoyé.")

    # Fermeture de la socket client
    client_socket.close()

# Point d'entrée du programme
if __name__ == "__main__":
    main()
