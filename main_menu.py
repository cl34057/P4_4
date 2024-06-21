# menu_principal.py

from menu_tournoi import gestion_tournoi
import sys

def main_menu():
    while True:
        print("===== Gestion des Joueurs et Tournois =====")
        print("1. Gestion des Joueurs")
        print("2. Gestion des Tournois")
        print("3. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            from menu_joueur import gestion_joueur  # Importation locale pour éviter la circularité
            gestion_joueur()
        elif choix == "2":
            gestion_tournoi()
        elif choix == "3":
            print("Merci d'avoir utilisé l'application. À bientôt !")
            sys.exit()  # Quitte l'application
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main_menu()
