from models.joueur_model import JoueurManager
from typing import Optional
import datetime

class JoueurController:
    def __init__(self):
        self.joueur_manager = JoueurManager()

    def ajouter_joueur(self, nom: str, prenom: str, date_naissance: datetime.date, elo: int) -> bool:
         return self.joueur_manager.ajouter_joueur(nom, prenom, date_naissance, elo)

    def modifier_joueur(self, index: int, nom: str, prenom: str, date_naissance: datetime.date, elo: int) -> None:
        self.joueur_manager.modifier_joueur(index, nom, prenom, date_naissance, elo)
        print("Joueur modifié avec succès.")

    def supprimer_joueur(self, index: int) -> None:
        self.joueur_manager.supprimer_joueur(index)
        print("Joueur supprimé avec succès.")

    def obtenir_liste_joueurs(self):
        return self.joueur_manager.joueurs

    def obtenir_joueur_par_index(self, index: int):
        if 0 < index <= len(self.joueur_manager.joueurs):
            return self.joueur_manager.joueurs[index - 1]
        return None

    def rechercher_joueur(self, nom: str, prenom: str) -> Optional[list]:
        return [joueur for joueur in self.joueur_manager.joueurs if joueur.nom == nom and joueur.prenom == prenom]
