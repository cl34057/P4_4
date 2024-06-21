import json
import os
from datetime import date, datetime
from typing import List
from models.joueur_model import Joueur
from models.match_model import Match
from models.ronde_model import Ronde

def date_encoder(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

class Tournoi:
    def __init__(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi, index=None):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_max_joueurs = nb_max_joueurs
        self.nb_rondes = nb_rondes
        self.type_tournoi = type_tournoi
        self.joueurs = []  # Liste pour les joueurs inscrits dans le tournoi
        self.rondes = []   # Liste pour les rondes du tournoi
        self.index = index  # Ajout de l'index
        
    def assigner_index(self, index):
        self.index = index

    def to_dict(self):
        return {
            "index": self.index,
            "nom": self.nom,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "nb_max_joueurs": self.nb_max_joueurs,
            "nb_rondes": self.nb_rondes,
            "type_tournoi": self.type_tournoi,
            "joueurs": [joueur.to_dict() for joueur in self.joueurs],
            "rondes": [ronde.to_dict() for ronde in self.rondes]
        }

    def mise_a_jour_fichier_json(self):
        filename = f"data/tournaments/{self.nom}.json"
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file, indent=4, default=date_encoder)

    def creer_ronde(self):
        if len(self.rondes) >= self.nb_rondes:
            print("Nombre maximal de rondes atteint pour ce tournoi.")
            return False
        
        nouvelle_ronde = Ronde(f"Ronde {len(self.rondes) + 1}")
        self.rondes.append(nouvelle_ronde)
        self.mise_a_jour_fichier_json()
        return True
        
    def ajouter_joueur_au_tournoi(self, joueurs: List[Joueur]):
        for joueur in joueurs:
            if joueur not in self.joueurs:
                self.joueurs.append(joueur)
        self.mise_a_jour_fichier_json()

    def supprimer_joueur_du_tournoi(self, joueur: Joueur):
        if joueur in self.joueurs:
            self.joueurs.remove(joueur)
            self.mise_a_jour_fichier_json()
            print(f"Le joueur {joueur.nom} a été supprimé du tournoi {self.nom}.")
        else:
            print(f"Le joueur {joueur.nom} n'est pas inscrit dans ce tournoi.")

    def charger_joueurs(self):
        filepath = f"data/tournaments/{self.nom}_joueurs.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                joueurs_data = json.load(file)
                self.joueurs = [Joueur(**data) for data in joueurs_data]

    def classement(self):
        classement = {joueur.nom: 0 for joueur in self.joueurs}
        for ronde in self.rondes:
            for match in ronde.matchs:
                if match.resultat == "blanc":
                    classement[match.joueur1.nom] += 1
                elif match.resultat == "noir":
                    classement[match.joueur2.nom] += 1
                elif match.resultat == "nul":
                    classement[match.joueur1.nom] += 0.5
                    classement[match.joueur2.nom] += 0.5
        classement = sorted(classement.items(), key=lambda item: item[1], reverse=True)
        return classement

#***************************************TournoiManager************************************************
class TournoiManager:
    def __init__(self, directory_path='data/tournaments'):
        self.directory_path = directory_path
        os.makedirs(self.directory_path, exist_ok=True)
        self.tournois = []
        self.charger_tournois()

    def charger_tournois(self):
        file_path = f"{self.directory_path}/tournois.json"
        try:
            with open(file_path, "r", encoding="utf-8") as fichier:
                data = json.load(fichier)
                self.tournois = [self.dict_to_tournoi(tournoi_data) for tournoi_data in data]
        except FileNotFoundError:
            print(f"Le fichier {file_path} n'existe pas.")

    def sauvegarder_tournois(self):
        file_path = f"{self.directory_path}/tournois.json"
        tournois_data = [tournoi.to_dict() for tournoi in self.tournois]
        with open(file_path, "w", encoding="utf-8") as fichier:
            json.dump(tournois_data, fichier, indent=4, default=date_encoder)

    def sauvegarder_tournoi(self, tournoi):
        file_path = f"{self.directory_path}/{tournoi.nom}.json"
        with open(file_path, "w", encoding="utf-8") as fichier:
            json.dump(tournoi.to_dict(), fichier, indent=4, default=date_encoder)
            
    def afficher_tous_les_tournois(self):
        return self.tournois  # Retourne la liste de tous les tournois
    def ajouter_tournoi(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
        # Trouver le dernier index utilisé
        dernier_index = max([tournoi.index for tournoi in self.tournois], default=0)
        nouvel_index = dernier_index + 1
        
        tournoi = Tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi, nouvel_index)
        self.tournois.append(tournoi)
        self.sauvegarder_tournois()
        return tournoi

    def modifier_tournoi(self, index, nom=None, date_debut=None, date_fin=None, nb_max_joueurs=None, nb_rondes=None, type_tournoi=None):
        if 0 <= index < len(self.tournois):
            tournoi = self.tournois[index]
            if nom:
                tournoi.nom = nom
            if date_debut:
                tournoi.date_debut = date_debut
            if date_fin:
                tournoi.date_fin = date_fin
            if nb_max_joueurs:
                tournoi.nb_max_joueurs = nb_max_joueurs
            if nb_rondes:
                tournoi.nb_rondes = nb_rondes
            if type_tournoi:
                tournoi.type_tournoi = type_tournoi
            self.sauvegarder_tournoi(tournoi)
        else:
            print("Index de tournoi invalide.")

    def ajouter_joueur_au_tournoi(self, index_tournoi, joueurs_selectionnes):
        if 0 <= index_tournoi < len(self.tournois):
            tournoi = self.tournois[index_tournoi]
            for joueur in joueurs_selectionnes:
                if joueur not in tournoi.joueurs:
                    tournoi.joueurs.append(joueur)
            self.sauvegarder_tournoi(tournoi)
        else:
            print("Index de tournoi invalide.")

    def dict_to_tournoi(self, data):
        nom = data.get('nom')
        date_debut = data.get('date_debut')
        date_fin = data.get('date_fin')
        nb_max_joueurs = data.get('nb_max_joueurs')
        nb_rondes = data.get('nb_rondes')
        type_tournoi = data.get('type_tournoi')
        index = data.get('index')
        joueurs = [Joueur(**joueur_data) for joueur_data in data.get('joueurs', [])]
        tournoi = Tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi, index)
        tournoi.joueurs = joueurs  # Ajout des joueurs au tournoi
        return tournoi

    def obtenir_classement_final(self, index_tournoi):
        if 0 <= index_tournoi < len(self.tournois):
            tournoi = self.tournois[index_tournoi]
            classement_final = {joueur.nom: 0 for joueur in tournoi.joueurs}
            for ronde in tournoi.rondes:
                for match in ronde.matchs:
                    if match.resultat == 'victoire_joueur1':
                        classement_final[match.joueur1.nom] += 1
                    elif match.resultat == 'victoire_joueur2':
                        classement_final[match.joueur2.nom] += 1
                    else:
                        classement_final[match.joueur1.nom] += 0.5
                        classement_final[match.joueur2.nom] += 0.5
            classement_final = sorted(classement_final.items(), key=lambda item: item[1], reverse=True)
            return classement_final
        else:
            print("Index de tournoi invalide.")
            return None
