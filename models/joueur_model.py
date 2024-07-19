import json
import os
import datetime
from typing import Optional, List, Dict

class Joueur:
    def __init__(self, index: int, nom: str, prenom: str, date_naissance: datetime.date, elo: int):
        self.index = index
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.elo = elo
        self.score = 0  # Initialiser le score à 0
    """def ajouter_points(self, points):
        self.score_cumule += points"""
        
    def to_dict(self) -> Dict:
        return {
            'index': self.index,
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance.isoformat(),
            'elo': self.elo,
           
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Joueur':
        return cls(
            index=data['index'],
            nom=data['nom'].split()[0],
            prenom=data['nom'].split()[1] if len(data['nom'].split()) > 1 else "",
            date_naissance=datetime.date.fromisoformat(data['date_naissance']),
            elo=data['elo']
        )
       
        

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Joueur):
            return NotImplemented
        return self.index == other.index

    def __str__(self) -> str:
        return f"{self.prenom} {self.nom} ({self.date_naissance}) - Elo: {self.elo}"
    def __hash__(self):
        return hash(self.index)
class JoueurManager:
    MAX_JOUEURS = 100
    FICHIER_JSON = "data/joueur.json"

    def __init__(self):
        self.joueurs: List[Joueur] = []
        self.charger_joueurs()

    def charger_joueurs(self) -> None:
        if os.path.exists(self.FICHIER_JSON):
            with open(self.FICHIER_JSON, "r") as file:
                data = json.load(file)
                self.joueurs = [Joueur.from_dict(joueur) for joueur in data]

    def sauvegarder_joueurs(self) -> None:
        with open(self.FICHIER_JSON, "w") as file:
            data = [joueur.to_dict() for joueur in self.joueurs]
            json.dump(data, file, indent=4)

    def ajouter_joueur(self, nom: str, prenom: str, date_naissance: datetime.date, elo: int) -> bool:
        joueur_existant = self.trouver_joueur_par_details(nom, prenom, date_naissance)
        if joueur_existant:
            print("Ce joueur existe déjà.")
            return False
        
        age_minimum = datetime.timedelta(days=7*365)
        if (datetime.date.today() - date_naissance) < age_minimum:
            print("Le joueur doit avoir au moins 7 ans pour s'inscrire.")
            return False

        if len(self.joueurs) < self.MAX_JOUEURS:
            index = len(self.joueurs) + 1
            nouveau_joueur = Joueur(index, nom, prenom, date_naissance, elo)
            self.joueurs.append(nouveau_joueur)
            self.sauvegarder_joueurs()
            print("Joueur ajouté avec succès.")
            return True
        else:
            print("Limite de joueurs atteinte. Impossible d'ajouter un nouveau joueur.")
            return False

    def modifier_joueur(self, index: int, nom: str, prenom: str, date_naissance: datetime.date, elo: int) -> None:
        if 0 < index <= len(self.joueurs):
            joueur = self.joueurs[index - 1]
            joueur.nom = nom
            joueur.prenom = prenom
            joueur.date_naissance = date_naissance
            joueur.elo = elo
            self.sauvegarder_joueurs()
        else:
            print("Index de joueur invalide.")

    def supprimer_joueur(self, index: int) -> None:
        if 0 < index <= len(self.joueurs):
            del self.joueurs[index - 1]
            for joueur in self.joueurs[index - 1:]:
                joueur.index -= 1
            self.sauvegarder_joueurs()
        else:
            print("Index de joueur invalide.")

    def trouver_joueur_par_details(self, nom: str, prenom: str, date_naissance: datetime.date) -> Optional[Joueur]:
        return next((joueur for joueur in self.joueurs 
                     if joueur.nom == nom and joueur.prenom == prenom and joueur.date_naissance == date_naissance), None)


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