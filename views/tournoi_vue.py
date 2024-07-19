import datetime
import re
import json
from controllers.tournoi_controller import TournoiController
from models.joueur_model import Joueur, JoueurManager

class TournoiVue:
    def __init__(self, tournoi_controller: TournoiController, joueur_manager: JoueurManager):
        self.tournoi_controller = tournoi_controller
        self.joueur_manager = joueur_manager

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
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index)

        if not tournoi:
            print("Tournoi non trouvé.")
            return

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
        try:
            with open('data/joueur.json', 'r') as f:
                tous_joueurs = json.load(f)
        except FileNotFoundError:
            print("Fichier data/joueur.json non trouvé.")
            return
        except json.JSONDecodeError:
            print("Erreur dans le format du fichier data/joueur.json.")
            return

        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if not tournoi:
            print('Tournoi non trouvé.')
            return

        print(f'Joueurs actuellement inscrits dans le tournoi {tournoi.nom}:')
        for joueur in tournoi.joueurs:
            print(f'- {joueur.nom} {joueur.prenom}')

        joueurs_inscrits_indices = [j.index for j in tournoi.joueurs]
        joueurs_disponibles = [j for j in tous_joueurs if j['index'] not in joueurs_inscrits_indices]

        print('\nJoueurs disponibles:')
        for joueur in joueurs_disponibles:
            print(f"{joueur['index']}. {joueur['nom']} {joueur['prenom']}")

        joueurs_selectionnes = []

        while len(tournoi.joueurs) + len(joueurs_selectionnes) < tournoi.nb_max_joueurs:
            try:
                choix = int(input('Entrez l\'index du joueur à ajouter (ou 0 pour terminer): '))
                if choix == 0:
                    break
                joueur = next((j for j in joueurs_disponibles if j['index'] == choix), None)
                if joueur and joueur not in joueurs_selectionnes:
                    joueurs_selectionnes.append(joueur)
                    print(f"Joueur {joueur['nom']} {joueur['prenom']} ajouté.")
                    joueurs_disponibles.remove(joueur)
                else:
                    print('Index invalide ou joueur déjà inscrit.')
            except ValueError:
                print('Veuillez entrer un nombre valide.')

        for joueur in joueurs_selectionnes:
            nouveau_joueur = Joueur(
                index=joueur['index'],
                nom=joueur['nom'],
                prenom=joueur['prenom'],
                date_naissance=datetime.date.fromisoformat(joueur['date_naissance']),
                elo=joueur['elo']
            )
            tournoi.ajouter_joueur(nouveau_joueur)

        tournoi.sauvegarder_joueurs()
        print('Joueurs ajoutés au tournoi avec succès.')

    def afficher_liste_tournois(self):
        print("===== Liste des tournois =====")
        for i, tournoi in enumerate(self.tournoi_controller.tournoi_manager.tournois, 1):
            print(f"{i}. {tournoi.nom} ({tournoi.date_debut} - {tournoi.date_fin})")

    def afficher_details_tournoi(self, index):
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index)
        if not tournoi:
            print("Tournoi non trouvé.")
            return None

        print(f"===== Détails du tournoi {tournoi.nom} =====")
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre maximal de joueurs : {tournoi.nb_max_joueurs}")
        print(f"Nombre de rondes : {tournoi.nb_rondes}")
        print(f"Type de tournoi : {tournoi.type_tournoi}")
        print(f"Joueurs inscrits ({len(tournoi.joueurs)}):")
        for joueur in tournoi.joueurs:
            print(f"- {joueur.nom} {joueur.prenom}")

        print("Rondes :")
        for ronde in tournoi.rondes:
            print(f"Ronde {ronde.numero} :")
            for match in ronde.matchs:
                print(f"- {match.joueur_blanc.nom} {match.joueur_blanc.prenom} vs {match.joueur_noir.nom} {match.joueur_noir.prenom} : {match.resultat}")

            print(f"Classement après la ronde {ronde.numero} :")
            for ligne in ronde.obtenir_classement_ronde():
                print(ligne)

        return tournoi

    def creer_ronde(self, index_tournoi):
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if not tournoi:
            print('Tournoi non trouvé.')
            return

        tournoi.jouer_ronde()
        self.tournoi_controller.tournoi_manager.sauvegarder_tournois()
        print("Ronde créée avec succès.")

    def supprimer_joueur_tournoi(self, index_tournoi: int):
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if not tournoi:
            print("Tournoi non trouvé.")
            return

        if not tournoi.joueurs:
            print("Aucun joueur n'est inscrit à ce tournoi.")
            return

        print(f"Joueurs inscrits au tournoi {tournoi.nom}:")
        for i, joueur in enumerate(tournoi.joueurs, 1):
            print(f"{i}. {joueur.nom} {joueur.prenom}")

        while True:
            try:
                choix = int(input("Entrez le numéro du joueur à supprimer (0 pour annuler) : "))
                if choix == 0:
                    print("Suppression annulée.")
                    return

                if 1 <= choix <= len(tournoi.joueurs):
                    joueur_a_supprimer = tournoi.joueurs[choix - 1]
                    if self.tournoi_controller.supprimer_joueur_du_tournoi(index_tournoi, joueur_a_supprimer):
                        print(f"Le joueur {joueur_a_supprimer.nom} {joueur_a_supprimer.prenom} a été supprimé du tournoi.")
                    else:
                        print("Erreur lors de la suppression du joueur.")
                    return
                else:
                    print("Numéro de joueur invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")