from models.joueur_model import JoueurManager
from config import MAX_JOUEURS

class JoueurController:
    # la variable self.joueur_manager est initialisée dans le constructeur de la classe JoueurController
    def __init__(self):
        self.joueur_manager = JoueurManager()

    def ajouter_joueur(self, nom, prenom, date_naissance, elo):
         return self.joueur_manager.ajouter_joueur(nom, prenom, date_naissance, elo)

    def modifier_joueur(self, index, nom, prenom, date_naissance, elo):
        self.joueur_manager.modifier_joueur(index, nom, prenom, date_naissance, elo)
        print("Joueur modifié avec succès.")

    def supprimer_joueur(self, index):
        self.joueur_manager.supprimer_joueur(index)
        print("Joueur supprimé avec succès.")
    