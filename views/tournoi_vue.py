import datetime
import re
from controllers.tournoi_controller import TournoiController
from models.joueur_model import JoueurManager
from models.tournoi_model import Tournoi

class TournoiVue:
    def __init__(self, tournoi_controller):
        self.tournoi_controller = tournoi_controller
        self.joueur_manager = JoueurManager()

    def afficher_menu(self):
        print("===== Menu Tournoi =====")
        print("1. Créer un nouveau tournoi")
        print("2. Modifier un tournoi")
        print("3. Supprimer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Afficher les détails d'un tournoi")
        print("6. Ajouter des joueurs à un tournoi")
        print("7. Supprimer des joueurs d'un tournoi")
        print("8. Gerer les rondes")
        print("9. Afficher le classement final")
        print("10. Retour")

    def saisir_tournoi(self):
        while True:
            try:
                self.afficher_liste_tournois()
                index = int(input("Entrez l'index du tournoi : "))
                if 1 <= index <= len(self.tournoi_controller.afficher_tous_les_tournois()):
                    return index
                else:
                    print("Index invalide. Veuillez entrer un index valide.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre.")
    def modifier_tournoi(self):
        index = self.saisir_tournoi() - 1
        tournoi = self.tournoi_controller.afficher_tous_les_tournois()[index]

        print("===== Modifier le tournoi =====")
        print(f"Nom du tournoi : {tournoi.nom}")
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre maximal de joueurs : {tournoi.nb_max_joueurs}")
        print(f"Nombre de rondes : {tournoi.nb_rondes}")
        print(f"Type de tournoi : {tournoi.type_tournoi}")

        choix_modification = input("Voulez-vous modifier ce tournoi ? (o/n) : ")

        if choix_modification.lower() == 'o':
            nom = input(f"Nouveau nom du tournoi ({tournoi.nom}) : ") or tournoi.nom
            date_debut = input(f"Nouvelle date de début ({tournoi.date_debut}) : ") or tournoi.date_debut
            date_fin = input(f"Nouvelle date de fin ({tournoi.date_fin}) : ") or tournoi.date_fin
            nb_max_joueurs = input(f"Nouveau nombre maximal de joueurs ({tournoi.nb_max_joueurs}) : ") or tournoi.nb_max_joueurs
            nb_rondes = input(f"Nouveau nombre de rondes ({tournoi.nb_rondes}) : ") or tournoi.nb_rondes
            type_tournoi = input(f"Nouveau type de tournoi ({tournoi.type_tournoi}) : ") or tournoi.type_tournoi

            print("Modifications proposées :")
            print(f"Nom du tournoi : {nom}")
            print(f"Date de début : {date_debut}")
            print(f"Date de fin : {date_fin}")
            print(f"Nombre maximal de joueurs : {nb_max_joueurs}")
            print(f"Nombre de rondes : {nb_rondes}")
            print(f"Type de tournoi : {type_tournoi}")

            confirmation = input("Confirmez-vous ces modifications ? (o/n) : ")
            if confirmation.lower() == 'o':
                self.tournoi_controller.modifier_tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
                print("Tournoi modifié avec succès.")
            else:
                print("Modification annulée.")
        else:
            print("Aucune modification effectuée.")

    def supprimer_joueur_tournoi(self, index_tournoi):
        tournoi = self.tournoi_controller.tournoi_manager.tournois[index_tournoi - 1]
        print("Joueurs inscrits :")
        for i, joueur in enumerate(tournoi.joueurs, start=1):
            print(f"{i}. {joueur.nom}")

        choix_joueur = int(input("Sélectionnez le numéro du joueur à supprimer : "))
        if 1 <= choix_joueur <= len(tournoi.joueurs):
            joueur = tournoi.joueurs.pop(choix_joueur - 1)
            self.tournoi_controller.supprimer_joueur_tournoi(index_tournoi, joueur)
            print(f"{joueur.nom} supprimé du tournoi.")
        else:
            print("Numéro de joueur invalide. Veuillez réessayer.")

    def afficher_liste_tournois(self):
        tournois = self.tournoi_controller.afficher_tous_les_tournois()
        if not tournois:
            print("Aucun tournoi trouvé.")
        else:
            print("Liste des tournois :")
            for i, tournoi in enumerate(tournois, 1):
                print(f"{i}. {tournoi.nom}")

    def afficher_details_tournoi(self, index):
        tournois = self.tournoi_controller.afficher_tous_les_tournois()
        if 0 <= index < len(tournois):
            tournoi = tournois[index]
            print(f"Détails du tournoi {tournoi.nom}:")
            print(f"Date de début: {tournoi.date_debut}")
            print(f"Date de fin: {tournoi.date_fin}")
            print(f"Nombre maximum de joueurs: {tournoi.nb_max_joueurs}")
            print(f"Nombre de rondes: {tournoi.nb_rondes}")
            print(f"Type de tournoi: {tournoi.type_tournoi}")
            print("Liste des joueurs inscrits:")
            for joueur in tournoi.joueurs:
                print(f"- {joueur.nom}")
            print("Rondes du tournoi:")
            for ronde in tournoi.rondes:
                print(f"- {ronde.nom}")
        else:
            print("Index de tournoi invalide.")
    def gerer_rondes_tournoi(self, index_tournoi):
        tournoi = self.tournoi_controller.tournoi_manager.tournois[index_tournoi - 1]
        print(f"Rondes actuelles du tournoi {tournoi.nom}:")
        for i, ronde in enumerate(tournoi.rondes, start=1):
            print(f"{i}. {ronde}")

        action = input("Souhaitez-vous ajouter ou supprimer une ronde ? (ajouter/supprimer/retour) : ").lower()
        
        if action == "ajouter":
            nouvelle_ronde = input("Nom de la nouvelle ronde : ")
            tournoi.rondes.append(nouvelle_ronde)
            print(f"Ronde {nouvelle_ronde} ajoutée au tournoi.")
        elif action == "supprimer":
            if tournoi.rondes:
                index_ronde = int(input("Entrez le numéro de la ronde à supprimer : "))
                if 1 <= index_ronde <= len(tournoi.rondes):
                    ronde_supprimee = tournoi.rondes.pop(index_ronde - 1)
                    print(f"Ronde {ronde_supprimee} supprimée du tournoi.")
                else:
                    print("Numéro de ronde invalide.")
            else:
                print("Aucune ronde à supprimer.")
        elif action == "retour":
            return
        else:
            print("Action non reconnue.")

    def afficher_classement_final(self, index):
        tournoi = self.tournoi_controller.tournoi_manager.tournois[index - 1]
        print(f"===== Classement final du tournoi {tournoi.nom} =====")
        classement = self.tournoi_controller.obtenir_classement_final(index)
        if not classement:
            print("Aucun classement disponible pour ce tournoi.")
            return
        print("Position | Joueur            | Points")
        print("-" * 40)
        for i, joueur_info in enumerate(classement, start=1):
            joueur = joueur_info['joueur']
            points = joueur_info['points']
            print(f"{i:<8} | {joueur.nom:<17} | {points}")

    def run(self):
        while True:
            self.afficher_menu()
            choix = input("Choisissez une option : ")

            if choix == "1":
                nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi = self.saisir_tournoi()
                self.tournoi_controller.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
                print("Tournoi créé avec succès.")
            elif choix == "2":
                self.modifier_tournoi()
            elif choix == "3":
                index = self.saisir_index_tournoi()
                self.tournoi_controller.supprimer_tournoi(index)
                print("Tournoi supprimé avec succès.")
            elif choix == "4":
                self.afficher_liste_tournois()
            elif choix == "5":
                index = self.saisir_index_tournoi()
                self.afficher_details_tournoi(index)
            elif choix == "6":
                index = self.saisir_index_tournoi()
                joueurs_ajoutes = self.saisir_joueurs_participants(index)
                for joueur in joueurs_ajoutes:
                    self.tournoi_controller.ajouter_joueur_tournoi(index, joueur)
            elif choix == "7":
                index = self.saisir_index_tournoi()
                self.supprimer_joueur_tournoi(index)
            elif choix == "8":
                index = self.saisir_index_tournoi()
                self.gerer_rondes_tournoi(index)
            elif choix == "9":
                index = self.saisir_index_tournoi()
                self.afficher_classement_final(index)
            elif choix == "10":
                print("Retour au menu principal.")
                break
            else:
                print("Option non valide. Veuillez entrer un chiffre entre 1 et 10.")
