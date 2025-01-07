# Communication-entre-deux-machines-virtuelles
Etablissement de réseaux entre deux machines virtuelles avec partage des fichiers avec wireshirk ,les adresses ip et les scripts pythons sur unubutu
# Communication entre deux machines virtuelles - Réseautage et partage de fichiers 🌐💻

## Description
Le projet **Communication entre deux machines virtuelles** consiste à établir un réseau entre deux machines virtuelles (VMs) afin de permettre la communication, le partage de fichiers et l'analyse du trafic réseau avec **Wireshark**. Ce projet est conçu pour simuler une communication entre deux systèmes Ubuntu en utilisant des adresses IP statiques et des scripts Python pour l'automatisation de certaines tâches.

Le projet montre comment configurer des réseaux entre des machines virtuelles, utiliser des outils de surveillance du réseau comme Wireshark, et comprendre les bases de la communication réseau dans un environnement virtuel.

## Fonctionnalités
- **Réseau entre machines virtuelles** : Connexion de deux machines virtuelles dans un réseau local, en utilisant des adresses IP statiques.
- **Partage de fichiers** : Mise en place d'un partage de fichiers entre les deux machines en utilisant des protocoles comme **SSH** ou **Samba**.
- **Analyse du réseau avec Wireshark** : Surveillance du trafic réseau entre les deux machines en utilisant **Wireshark** pour capturer et analyser les paquets.
- **Scripts Python pour automatisation** : Utilisation de scripts Python pour automatiser certaines tâches comme l'envoi et la réception de fichiers via réseau.
  
## Technologies utilisées
- **Machines virtuelles (VMs)** : Utilisation d'outils comme **VirtualBox** ou **VMware** pour créer et gérer les VMs.
- **Ubuntu** : Système d'exploitation utilisé sur les machines virtuelles.
- **Wireshark** : Outil de capture et d'analyse de paquets réseau.
- **Python** : Langage utilisé pour automatiser le transfert de fichiers et d'autres tâches réseau.
- **SSH / Samba** : Protocoles utilisés pour le partage de fichiers entre les VMs.

## Architecture du projet
Le projet consiste en deux machines virtuelles connectées à un réseau local (LAN), avec un serveur SSH ou Samba configuré sur chacune pour permettre le partage de fichiers. Un script Python sera utilisé pour transférer des fichiers entre les machines, et Wireshark sera utilisé pour capturer le trafic réseau.

1. **Machine virtuelle 1 (VM1)** : Serveur SSH ou Samba configuré pour permettre le partage de fichiers.
2. **Machine virtuelle 2 (VM2)** : Client Python qui envoie des fichiers à VM1.
3. **Wireshark** : Capturer et analyser le trafic réseau entre les deux machines.

## Installation

### Prérequis
1. **VirtualBox** ou **VMware** : Pour créer les machines virtuelles.
2. **Ubuntu** : Installer **Ubuntu 20.04** ou version plus récente sur chaque machine virtuelle.
3. **Wireshark** : Outil de capture de paquets réseau installé sur l'une des machines.
4. **Python** : Installer **Python 3.x** sur les deux machines pour utiliser les scripts.
5. **SSH ou Samba** : Configurer un serveur **SSH** ou **Samba** sur les machines pour le partage de fichiers.

### Étapes d'installation

1. **Création des machines virtuelles** :
   - Créez deux machines virtuelles avec **Ubuntu** installé sur chaque machine. Assurez-vous qu'elles sont sur le même réseau local (en utilisant un adaptateur réseau en mode "réseau privé" ou "réseau interne").
   - Attribuez des adresses IP statiques à chaque machine (par exemple, 192.168.1.10 et 192.168.1.20).

2. **Installation de Wireshark** :
   - Sur l'une des machines, installez **Wireshark** pour capturer le trafic réseau.
   ```bash
   sudo apt update
   sudo apt install wireshark
