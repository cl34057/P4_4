import json
import os
import datetime
from config import MAX_JOUEURS
from typing import Optional
class Joueur:
    def __init__(self, index, nom: str, prenom: str, date_naissance: datetime.date, elo: int):
        self.index = index
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.elo = elo
    # renvoie un dictionnaire contenant les attributs de l'objet.
    def __dict__(self):
        return {
            'index': self.index,
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': str(self.date_naissance),
            'elo': self.elo
        }
    # une méthode de classe from_dict() qui permet de créer un objet Joueur à partir d'un dictionnaire.
    @classmethod
    def from_dict(cls, data):
        return cls(
            index=data['index'],
            nom=data['nom'],
            prenom=data['prenom'],
            date_naissance=datetime.datetime.strptime(data['date_naissance'], '%Y-%m-%d').date(),
            elo=data['elo']
        )
     # differencier 2 joueurs par leur nom , puis leur prénom et si identiques, par leur    
    def __eq__(self, other):    #__eq__ dans la classe Joueur, qui est utilisée pour vérifier si deux joueurs sont égaux
        return (
            self.nom == other.nom and 
            self.prenom == other.prenom and 
            self.date_naissance == other.date_naissance
        )

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.date_naissance}) - Elo: {self.elo}"

class JoueurManager:
    MAX_JOUEURS = 100
    FICHIER_JSON = "data/joueur.json"

    def __init__(self):
        self.joueurs = []
        self.charger_joueurs()

    def charger_joueurs(self):
        if os.path.exists(self.FICHIER_JSON):
            with open(self.FICHIER_JSON, "r") as file:
                data = json.load(file)
                self.joueurs = [self.convertir_dict_vers_joueur(joueur) for joueur in data]

    def sauvegarder_joueurs(self):
        with open(self.FICHIER_JSON, "w") as file:
            data = [self.convertir_joueur_vers_dict(joueur) for joueur in self.joueurs]
            json.dump(data, file, indent=4)

    def ajouter_joueur(self, nom, prenom, date_naissance, elo):
       
        # Vérifier si le joueur existe déjà
        joueur_existant = self.trouver_joueur_par_details(nom, prenom, date_naissance)
        if joueur_existant:
            print("Ce joueur existe déjà.")
            return False
        
        # Vérifier si le joueur a au moins 7 ans
        date_actuelle = datetime.date.today()
        age_minimum = datetime.timedelta(days=7*365)  # 7 ans en jours
        age_joueur = date_actuelle - date_naissance
        if age_joueur < age_minimum:
            print("Le joueur doit avoir au moins 7 ans pour s'inscrire.")
            return False

        # Ajouter le nouveau joueur
        if len(self.joueurs) < self.MAX_JOUEURS:
            index = len(self.joueurs) + 1  # Index basé sur la longueur actuelle de la liste des joueurs
            nouveau_joueur = Joueur(index, nom, prenom, date_naissance, elo)
            self.joueurs.append(nouveau_joueur)
            self.sauvegarder_joueurs()
            print("Joueur ajouté avec succès.")
            return True
        else:
            print("Limite de joueurs atteinte. Impossible d'ajouter un nouveau joueur.")
            return False
    def modifier_joueur(self, index, nom, prenom, date_naissance, elo):
        self.joueurs[index - 1].nom = nom
        self.joueurs[index - 1].prenom = prenom
        self.joueurs[index - 1].date_naissance = date_naissance
        self.joueurs[index - 1].elo = elo
        self.sauvegarder_joueurs()

    def supprimer_joueur(self, index):
        del self.joueurs[index - 1]
        # Mettre à jour les index des joueurs suivant le joueur supprimé
        for joueur in self.joueurs[index - 1:]:
            joueur.index -= 1
        self.sauvegarder_joueurs()

    def trouver_joueur_par_details(self, nom: str, prenom: str, date_naissance: datetime.date) -> Optional[Joueur]:
        # Parcourir tous les joueurs pour trouver un joueur avec les mêmes détails
        for joueur in self.joueurs:
            if joueur.nom == nom and joueur.prenom == prenom:
                # Assurez-vous que les dates de naissance sont au format datetime.date pour une comparaison précise
                if isinstance(joueur.date_naissance, str):
                    joueur_date = datetime.datetime.strptime(joueur.date_naissance, '%Y-%m-%d').date()
                else:
                    joueur_date = joueur.date_naissance
                
                if joueur_date == date_naissance:
                    return joueur
        # Si aucun joueur correspondant trouvé, retourner None
        return None



    def convertir_joueur_vers_dict(self, joueur):
        return {
            'index': joueur.index,
            'nom': joueur.nom,
            'prenom': joueur.prenom,
            'date_naissance': joueur.date_naissance.isoformat() if isinstance(joueur.date_naissance, datetime.date) else joueur.date_naissance,
            'elo': joueur.elo
        }

    def convertir_dict_vers_joueur(self, data):
        return Joueur(data['index'], data['nom'], data['prenom'], 
                      datetime.datetime.strptime(data['date_naissance'], '%Y-%m-%d').date() if isinstance(data['date_naissance'], str) else data['date_naissance'], 
                      data['elo'])
