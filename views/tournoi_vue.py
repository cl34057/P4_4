import datetime
import re
from controllers.tournoi_controller import TournoiController
from models.joueur_model import JoueurManager
from models.tournoi_model import TournoiManager  # Importez la classe TournoiManager

class TournoiVue:
    def __init__(self):
        self.tournoi_controller = TournoiController()
        self.joueur_manager = JoueurManager()

    def afficher_menu(self):
        print("===== Menu Tournoi =====")
        print("1. Créer un nouveau tournoi")
        print("2. Modifier un tournoi")
        print("3. Supprimer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Afficher les détails d'un tournoi")
        print("6. Retour")

    def saisir_tournoi(self):
        while True:
            nom = input("Nom du tournoi : ")
            if not re.match("^[a-zA-Z0-9 ]+$", nom):
                print("Le nom du tournoi doit contenir uniquement des caractères alphanumériques et peut contenir des espaces.")
                continue
            date_debut = input("Date de début (format YYYY-MM-DD) : ")
            date_fin = input("Date de fin (format YYYY-MM-DD) : ")
            try:
                date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
                date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
                if date_fin < date_debut:
                    print("La date de fin doit être ultérieure à la date de début.")
                    continue
                nb_max_joueurs = int(input("Nombre maximal de joueurs : "))
                nb_rondes = int(input("Nombre de rondes : "))
                type_tournoi = input("Type de tournoi : ")
                return nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi
            except ValueError:
                print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")

    def modifier_tournoi(self):
        index = self.saisir_index_tournoi()
        tournoi = self.tournoi_controller.tournoi_manager.tournois[index - 1]

        print("===== Modifier le tournoi =====")
        print(f"Nom du tournoi : {tournoi.nom}")
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre maximal de joueurs : {tournoi.nb_max_joueurs}")
        print(f"Nombre de rondes : {tournoi.nb_rondes}")
        print(f"Type de tournoi : {tournoi.type_tournoi}")

        choix_modification = input("Voulez-vous modifier ce tournoi ? (o/n) : ")

        if choix_modification.lower() == 'o':
            # Demander à l'utilisateur de saisir de nouvelles valeurs pour les attributs existants
            nom = input(f"Nouveau nom du tournoi ({tournoi.nom}) : ") or tournoi.nom
            date_debut = input(f"Nouvelle date de début ({tournoi.date_debut}) : ") or tournoi.date_debut
            date_fin = input(f"Nouvelle date de fin ({tournoi.date_fin}) : ") or tournoi.date_fin

            # Demander à l'utilisateur de saisir de nouvelles valeurs pour les attributs supplémentaires
            nb_max_joueurs = input(f"Nouveau nombre maximal de joueurs ({tournoi.nb_max_joueurs}) : ") or tournoi.nb_max_joueurs
            nb_rondes = input(f"Nouveau nombre de rondes ({tournoi.nb_rondes}) : ") or tournoi.nb_rondes
            type_tournoi = input(f"Nouveau type de tournoi ({tournoi.type_tournoi}) : ") or tournoi.type_tournoi

            # Afficher les modifications proposées
            print("Modifications proposées :")
            print(f"Nom du tournoi : {nom}")
            print(f"Date de début : {date_debut}")
            print(f"Date de fin : {date_fin}")
            print(f"Nombre maximal de joueurs : {nb_max_joueurs}")
            print(f"Nombre de rondes : {nb_rondes}")
            print(f"Type de tournoi : {type_tournoi}")

            # Confirmer les modifications avant de les enregistrer définitivement
            confirmation = input("Confirmez-vous ces modifications ? (o/n) : ")
            if confirmation.lower() == 'o':
                self.tournoi_controller.modifier_tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
                print("Tournoi modifié avec succès.")
            else:
                print("Modification annulée.")
        else:
            print("Aucune modification effectuée.")

    def saisir_index_tournoi(self):
        while True:
            try:
                self.afficher_liste_tournois()
                index = int(input("Entrez l'index du tournoi : "))
                if 1 <= index <= len(self.tournoi_controller.tournoi_manager.tournois):
                    return index
                else:
                    print("Index invalide. Veuillez entrer un index valide.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre.")

    def saisir_joueurs_participants(self, index_tournoi):
        joueurs_disponibles = self.joueur_manager.joueurs
        tournoi = self.tournoi_controller.tournoi_manager.tournois[index_tournoi - 1]
        print(f"Joueurs actuellement inscrits dans le tournoi {tournoi.nom}:")
        for joueur in tournoi.joueurs:
            print(f"- {joueur.nom}")

        print("Joueurs disponibles:")
        for i, joueur in enumerate(joueurs_disponibles):
            print(f"{i+1}. {joueur.nom}")

        joueurs_selectionnes = []
        while len(joueurs_selectionnes) < tournoi.nb_max_joueurs - len(tournoi.joueurs):
            try:
                index_joueur = int(input("Entrez l'index du joueur à ajouter (ou 0 pour terminer): "))
                if index_joueur == 0:
                    break
                if 1 <= index_joueur <= len(joueurs_disponibles):
                    joueur_selectionne = joueurs_disponibles[index_joueur - 1]
                    if joueur_selectionne not in tournoi.joueurs and joueur_selectionne not in joueurs_selectionnes:
                        joueurs_selectionnes.append(joueur_selectionne)
                        print(f"Joueur {joueur_selectionne.nom} ajouté.")
                    else:
                        print("Joueur déjà inscrit.")
                else:
                    print("Index invalide.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre.")
        return joueurs_selectionnes
    def afficher_liste_tournois(self):
        print("===== Liste des tournois =====")
        for i, tournoi in enumerate(self.tournoi_controller.tournoi_manager.tournois, 1):
            print(f"{i}. {tournoi.nom} ({tournoi.date_debut} - {tournoi.date_fin})")


    def afficher_details_tournoi(self, index):
        tournoi = self.tournoi_controller.tournoi_manager.tournois[index - 1]
        print(f"===== Détails du tournoi {tournoi.nom} =====")
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre maximal de joueurs : {tournoi.nb_max_joueurs}")
        print(f"Nombre de rondes : {tournoi.nb_rondes}")
        print(f"Type de tournoi : {tournoi.type_tournoi}")
        print("Joueurs inscrits :")
        for joueur in tournoi.joueurs:
            print(f"- {joueur.nom}")
        print("Rondes :")
        for ronde in tournoi.rondes:
            print(f"- {ronde}")

