from models.joueur_model import Joueur, JoueurManager
from controllers.joueur_controller import JoueurController
import datetime
from config import MAX_JOUEURS




class JoueurVue:
    #changez l'import de gestion_joueur pour une injection de dépendance (au lieu de from gestion_joueur import gestion_joueur) ):
    def __init__(self, gestion_joueur):
        self.gestion_joueur = gestion_joueur  # Attribuez la fonction à un attribut de l'objet
        self.joueur_controller = JoueurController()
        
    def afficher_menu(self):
        print("===== Menu Joueur =====")
        print("1. Ajouter un joueur")
        print("2. Modifier un joueur")
        print("3. Supprimer un joueur")
        print("4. Afficher la liste des joueurs")
        print("5. Afficher les détails d'un joueur")
        print("6. Retour")





    def saisir_joueur(self):
        while True:
            if len(self.joueur_controller.joueur_manager.joueurs) >= MAX_JOUEURS:
                print("Nombre maximal de joueurs atteint.")
                return None
            
            while True:
                nom = input("Nom du joueur : ")
                if not nom.isalpha():
                    print("Le nom doit contenir uniquement des lettres.")
                    continue
                break
            
            while True:
                prenom = input("Prénom du joueur : ")
                if not prenom.isalpha():
                    print("Le prénom doit contenir uniquement des lettres.")
                    continue
                break
            
            while True:
                date_naissance_str = input("Date de naissance du joueur (format YYYY-MM-DD) : ")
                try:
                    date_naissance = datetime.datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
                    break
                except ValueError:
                    print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")
                    continue
            
            while True:
                elo = input("Elo du joueur (entre 1000 et 3500) : ")
                if not elo.isdigit():
                    print("Le score Elo doit être un entier.")
                    continue
                elif not 1000 <= int(elo) <= 3500:
                    print("Le score Elo doit être compris entre 1000 et 3500.")
                    continue
                else:
                    break
                
            # Vérifier si le joueur existe déjà
            joueur_existant = self.joueur_controller.joueur_manager.trouver_joueur_par_details(nom, prenom, date_naissance)
            if joueur_existant:
                choix = input("CE JOUEUR EXISTE DÉJA. Voulez-vous ajouter un autre joueur ? (o/n) : ")
                if choix.lower() == 'o':
                    continue  # Revenir à la saisie du nouveau joueur
                elif choix.lower() == 'n':
                    # Revenir au menu joueur
                    print("Retour au menu joueur.")
                    self.gestion_joueur()  # Appeler la fonction gestion_joueur pour revenir au menu joueur
                    return  # Appeler la fonction gestion_joueur pour revenir au menu joueur
                else:
                    print("Choix invalide. Veuillez répondre par 'o' ou 'n'.")
                    continue
            elif choix.lower() == '6':
                # Si l'utilisateur choisit l'option 6, retournez au menu principal en appelant la fonction main_menu
                print("Retour au menu principal.")
                main_menu()
                return
            else:
                # Ajouter le joueur s'il n'existe pas déjà
                index = len(self.joueur_controller.joueur_manager.joueurs) + 1
                joueur = Joueur(index, nom, prenom, date_naissance, int(elo))
                self.joueur_controller.ajouter_joueur(joueur.nom, joueur.prenom, joueur.date_naissance, joueur.elo)
                
                # Demander si l'utilisateur veut ajouter un autre joueur
                choix = input("Voulez-vous ajouter un autre joueur ? (o/n) : ")
                if choix.lower() == 'o':
                    continue  # Revenir à la saisie du nouveau joueur
                elif choix.lower() == 'n':
                    # Revenir au menu joueur
                    print("Retour au menu joueur.")
                    self.gestion_joueur()  # Appeler la fonction gestion_joueur pour revenir au menu joueur
                    return 
                else:
                    print("Choix invalide. Veuillez répondre par 'o' ou 'n'.")
                    continue



    def modifier_joueur(self):
        
        index = self.saisir_index_joueur()
        joueur = self.joueur_controller.joueur_manager.joueurs[index - 1]

        print("===== Modifier le joueur =====")
        print(f"Nom : {joueur.nom}")
        print(f"Prénom : {joueur.prenom}")
        print(f"Date de naissance : {joueur.date_naissance}")
        print(f"Elo : {joueur.elo}")

        choix_modification = input("Voulez-vous modifier ce joueur ? (o/n) : ")

        if choix_modification.lower() == 'o':
            nom = input(f"Nouveau nom ({joueur.nom}) : ") or joueur.nom
            prenom = input(f"Nouveau prénom ({joueur.prenom}) : ") or joueur.prenom
            date_naissance = input(f"Nouvelle date de naissance ({joueur.date_naissance}) : ") or joueur.date_naissance
            elo = input(f"Nouvel elo ({joueur.elo}) : ") or joueur.elo

            self.joueur_controller.modifier_joueur(index, nom, prenom, date_naissance, elo)
            print("Joueur modifié avec succès.")
        else:
            print("Aucune modification effectuée.")
    def afficher_joueur(self, joueur):
        print("===== Affichage des détails d'un joueur =====")
        print("Nom :", joueur.nom)  # Afficher le nom
        print("Prénom :", joueur.prenom)
        print("Date de naissance :", joueur.date_naissance)
        print("Elo :", joueur.elo)

    def afficher_liste_joueurs(self):
        joueurs = self.joueur_controller.joueur_manager.joueurs
        print("===== Liste des Joueurs =====")
        for joueur in joueurs:
            print(f"Index: {joueurs.index(joueur) + 1}, Nom: {joueur.nom}, Prénom: {joueur.prenom}, Date_naissance: {joueur.date_naissance}, Elo: {joueur.elo}")

    def saisir_index_joueur(self):
        while True:
            try:
                index = int(input("Entrez l'index du joueur : "))
                if index < 1 or index > len(self.joueur_controller.joueur_manager.joueurs):
                    print("Index invalide. Veuillez entrer un index valide.")
                    continue
                else:
                    return index
            except ValueError:
                print("Veuillez entrer un nombre entier.")

    def saisir_joueur_details(self):
        while True:
            nom = input("Nouveau nom du joueur : ")
            if not nom.isalpha():
                print("Le nom doit contenir uniquement des lettres.")
                continue
            
            prenom = input("Nouveau prénom du joueur : ")
            if not prenom.isalpha():
                print("Le prénom doit contenir uniquement des lettres.")
                continue
            
            while True:
                date_naissance = input("Nouvelle date de naissance du joueur (format YYYY-MM-DD) : ")
                try:
                    datetime.datetime.strptime(date_naissance, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")
                    continue
            
            while True:
                elo = input("Nouveau Elo du joueur (entre 1000 et 3500) : ")
                if not elo.isdigit():
                    print("Le score Elo doit être un entier.")
                    continue
                elif not 1000 <= int(elo) <= 3500:
                    print("Le score Elo doit être compris entre 1000 et 3500.")
                    continue
                else:
                    break
                
            return nom, prenom, date_naissance, int(elo)
    def supprimer_joueur(self):
        index = self.saisir_index_joueur()
        self.joueur_controller.supprimer_joueur(index)
        print("Joueur supprimé avec succès.")
    
    def afficher_details_joueur(self):
        index = self.saisir_index_joueur()
        joueur = self.joueur_controller.joueur_manager.joueurs[index - 1]
        self.afficher_joueur(joueur)