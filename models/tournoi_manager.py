import datetime
import json
import os
from typing import List, Optional
from models.tournoi_model import Tournoi
from models.joueur_model import Joueur

class TournoiManager:
    MAX_TOURNOIS = 30

    def __init__(self):
        self.tournois: List[Tournoi] = []
        self.charger_tournois()
    # charger les tournois
    def charger_tournois(self):
        fichier_json = "data/tournaments.json"
        if os.path.exists(fichier_json):
            with open(fichier_json, "r", encoding='utf-8') as file:
                data = json.load(file)
                self.tournois = [Tournoi.from_dict(tournoi_data) for tournoi_data in data.values()]
            self.reindexer_tournois()

    def sauvegarder_tournois(self):
        fichier_json = "data/tournaments.json"
        data = {tournoi.nom: tournoi.to_dict() for tournoi in self.tournois}
        with open(fichier_json, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def trouver_tournoi_par_index(self, index: int) -> Optional[Tournoi]:
        return next((t for t in self.tournois if t.index == index), None)

    def ajouter_tournoi(self, nom: str, date_debut: datetime.date, date_fin: datetime.date, 
                        nb_max_joueurs: int, nb_rondes: int, type_tournoi: str) -> Optional[Tournoi]:
        if len(self.tournois) >= self.MAX_TOURNOIS:
            print("Nombre maximum de tournois atteint.")
            return None
        
        try:
            index = max((tournoi.index for tournoi in self.tournois), default=0) + 1
            nouveau_tournoi = Tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
            self.tournois.append(nouveau_tournoi)
            self.sauvegarder_tournois()
            print(f"Tournoi '{nom}' ajouté avec succès.")
            return nouveau_tournoi
        except Exception as e:
            print(f"Erreur lors de l'ajout du tournoi : {str(e)}")
            return None
    def supprimer_tournoi(self, index_tournoi: int) -> bool:
        if 0 <= index_tournoi < len(self.tournois):
            tournoi = self.tournois[index_tournoi]
            
            fichier_tournoi = f"data/tournaments/{tournoi.nom.replace(' ', '_')}.json"
            if os.path.exists(fichier_tournoi):
                os.remove(fichier_tournoi)

            fichier_joueurs = f"data/tournaments/{tournoi.nom.replace(' ', '_')}_joueurs.json"
            if os.path.exists(fichier_joueurs):
                os.remove(fichier_joueurs)

            del self.tournois[index_tournoi]
            self.reindexer_tournois()
            self.sauvegarder_tournois()
            return True
        else:
            print(f"Erreur : L'index {index_tournoi} est invalide.")
            return False

    def reindexer_tournois(self):
        for i, tournoi in enumerate(self.tournois):
            tournoi.index = i + 1  # Les index commencent à 1

    def ajouter_joueur_au_tournoi(self, index_tournoi: int, joueur: dict) -> bool:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)
        if tournoi:
            nouveau_joueur = Joueur(
                index=joueur['index'],
                nom=joueur['nom'],
                prenom=joueur['prenom'],
                date_naissance=datetime.datetime.strptime(joueur['date_naissance'], '%Y-%m-%d').date(),
                elo=joueur['elo']
            )
            if tournoi.ajouter_joueur(nouveau_joueur):
                self.sauvegarder_tournois()
                return True
        return False
    def supprimer_joueur_du_tournoi(self, joueur: Joueur) -> bool:
        if joueur in self.joueurs:
            self.joueurs.remove(joueur)
            self.nombre_inscrits = len(self.joueurs)
            self.sauvegarder_joueurs()
            return True
        return False
    def supprimer_joueur_tournoi(self, index_tournoi: int, joueur: Joueur) -> bool:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)
        if tournoi:
            return tournoi.supprimer_joueur(joueur)
        return False

    def creer_ronde(self, index_tournoi: int) -> bool:
        """Crée une nouvelle ronde pour un tournoi."""
        tournoi = self.trouver_tournoi_par_index(index_tournoi)
        if tournoi and tournoi.creer_ronde():
            self.sauvegarder_tournois()
            return True
        return False

    def obtenir_classement_tournoi(self, index_tournoi: int) -> List[tuple]:
        """Obtient le classement final d'un tournoi."""
        tournoi = self.trouver_tournoi_par_index(index_tournoi)
        return tournoi.classement() if tournoi else []

    def exporter_tournoi(self, index_tournoi: int, format: str = 'json') -> bool:
        """Exporte les données d'un tournoi."""
        tournoi = self.trouver_tournoi_par_index(index_tournoi)
        if not tournoi:
            return False
        
        if format == 'json':
            fichier = f"exports/{tournoi.nom}_export.json"
            with open(fichier, 'w') as f:
                json.dump(tournoi.to_dict(), f, indent=4, default=str)
            return True
        else:
            print(f"Format d'export '{format}' non supporté.")
            return False

    def importer_tournoi(self, fichier: str) -> Optional[Tournoi]:
        """Importe un tournoi depuis un fichier JSON."""
        if not os.path.exists(fichier):
            print(f"Le fichier {fichier} n'existe pas.")
            return None

        try:
            with open(fichier, 'r') as f:
                data = json.load(f)
            
            nouveau_tournoi = Tournoi(
                len(self.tournois) + 1,
                data.get('nom_tournoi', 'Tournoi sans nom'),
                datetime.datetime.fromisoformat(data.get('date_debut', '2000-01-01')).date(),
                datetime.datetime.fromisoformat(data.get('date_fin', '2000-01-02')).date(),
                int(data.get('nb_max_joueurs', 0)),
                int(data.get('nb_rondes', 0)),
                data.get('type_tournoi', 'Type inconnu')
            )
            self.tournois.append(nouveau_tournoi)
            self.sauvegarder_tournois()
            return nouveau_tournoi
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erreur lors de l'importation du tournoi : {str(e)}")
            return None