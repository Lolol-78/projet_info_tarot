import socket
import threading
import pickle
import time
import random

import joueur


class PartieTarot:
    
    def __init__(self, numero_lobby) -> None:
        # un joueur c'est (socket.socket, addr, username, joueur.Joueur)
        self.joueurs = []
        # dans nouveaux joueurs, on rajoute les nouveaux participants, de la forme (socket.socket, addresse, username)
        self.nouveaux_joueurs = []
        self.numero_lobby = numero_lobby
        self.a_commence = False
        self.prises = []
    
    def run(self):
        while len(self.joueurs) != 4:
            if self.nouveaux_joueurs != []:
                for nv_joueur in self.nouveaux_joueurs:
                    self.send_msg_to_all("action", "nouveau_joueur_dans_lobby", nv_joueur[2])
                    self.joueurs.append(nv_joueur + (joueur.Joueur(),))
                    self.send_msg(nv_joueur[0], "message", f"Tu as rejoint le lobby {self.numero_lobby}")
                self.nouveaux_joueurs.clear()
        self.send_msg_to_all("message", 'Tous les joueurs sont connectes, la partie commence')
        self.a_commence = True
        self.distribuer()
        self.faire_le_choix_des_prises()
        while 1: pass
    
    def send_msg_to_all(self, type, *msg):
        for connection in self.joueurs:
            msg_send = pickle.dumps(('LOBBY', type, *msg))
            connection[0].send(msg_send)
        time.sleep(0.1)
    
    def send_msg(self, conn, type, *msg):
        msg_send = pickle.dumps(('LOBBY', type, *msg))
        conn.send(msg_send)
        time.sleep(0.1)
        

    def distribuer(self):
        jeu=[ ('coeur', 1), ('coeur', 2), ('coeur', 3),('coeur', 4),('coeur', 5),('coeur', 6),('coeur', 7),('coeur', 8),('coeur', 9), ('coeur', 10), ('coeur', 11), ('coeur', 12), ('coeur', 13), ('coeur', 14), ('pique', 1), ('pique', 2), ('pique', 3), ('pique', 4), ('pique', 5), ('pique', 6), ('pique', 7), ('pique', 8), ('pique', 9), ('pique', 10), ('pique', 11), ('pique', 12), ('pique', 13), ('pique', 14), ('carreau', 1), ('carreau', 2), ('carreau', 3), ('carreau', 4), ('carreau', 5), ('carreau', 6), ('carreau', 7), ('carreau', 8), ('carreau', 9), ('carreau', 10), ('carreau', 11), ('carreau', 12), ('carreau', 13), ('carreau', 14), ('trèfle', 1), ('trèfle', 2), ('trèfle', 3), ('trèfle', 4), ('trèfle', 5), ('trèfle', 6), ('trèfle', 7), ('trèfle', 8), ('trèfle', 9), ('trèfle', 10), ('trèfle', 11), ('trèfle', 12), ('trèfle', 13), ('trèfle', 14), ('atout',1),('atout',2),('atout',3),('atout',4),('atout',5),('atout',6),('atout',7),('atout',8),('atout',9),('atout',10),('atout',11),('atout',12),('atout',13),('atout',14),('atout',15),('atout',16),('atout',17),('atout',18),('atout',19),('atout',20),('atout',21),('atout',0)]
        a=0
        for i in range (4):
            self.joueurs[i][3].main=[]
        for j in range (4):
            for k in range(18):
                d=random.randint(0,77-k-a)
                self.joueurs[j][3].main.append(jeu[d])
                jeu.pop(d)
            a+=18    
        self.chien=jeu
        for i in range(4):
            print(self.joueurs[i][3].main)
        for i in range(4):
            self.send_msg(self.joueurs[i][0], 'action', 'recevoir_jeu', self.joueurs[i][3].main)
        self.send_msg_to_all("action", "verifier_reception_jeu")

    def faire_le_choix_des_prises(self):
        nb_prise_actuel = 0
        for i in range(4):
            self.send_msg(self.joueurs[i][0], 'action', 'choisir_prise', self.prises)
            while len(self.prises) == nb_prise_actuel:
                pass
            nb_prise_actuel = len(self.prises)
        self.send_msg_to_all("message", f'les prises sont {self.prises}')
    
    def recevoir_prise(self, username, prise):
        self.send_msg_to_all("message", f"{username} {'fait une '+('petite', 'garde', 'garde-sans', 'garde-contre')[prise-1] if prise != 0 else 'passe'}!")
        self.prises.append(prise)
    
    def jeu_pas_recu(self, username):
        for joueur in self.joueurs:
            if joueur[2] == username:
                self.send_msg(joueur[0], "action", "recevoir_jeu", joueur[3].main)

