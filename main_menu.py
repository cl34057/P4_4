from menu_tournoi import gestion_tournoi
from controllers.tournoi_controller import TournoiController
from models.joueur_model import JoueurManager
from views.tournoi_vue import TournoiVue
import sys

def main_menu():
    tournoi_controller = TournoiController()
    joueur_manager = JoueurManager()
    tournoi_vue = TournoiVue(tournoi_controller, joueur_manager)
    
    while True:
        print("===== Gestion des Joueurs et Tournois =====")
        print("1. Gestion des Joueurs")
        print("2. Gestion des Tournois")
        print("3. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            from menu_joueur import gestion_joueur
            gestion_joueur()
        elif choix == "2":
            gestion_tournoi(tournoi_vue)  # Passez tournoi_vue ici
        elif choix == "3":
            print("Merci d'avoir utilisé l'application. À bientôt !")
            sys.exit()
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main_menu()