from models.tournoi_model import TournoiManager
from views.tournoi_vue import TournoiVue
from controllers.joueur_controller import JoueurController
def gestion_tournoi():
    tournoi_manager = TournoiManager()  # Initialisation du gestionnaire de tournois
    tournoi_vue = TournoiVue(tournoi_manager)  # Initialisation de la vue tournoi avec le gestionnaire de tournois
    joueur_controller = JoueurController()
    while True:
        print("\n===== Menu Tournoi =====")
        print("1. Créer un nouveau tournoi")
        print("2. Modifier un tournoi")
        print("3. Supprimer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Afficher les détails d'un tournoi")
        print("6. Ajouter des joueurs à un tournoi")
        print("7. Supprimer des joueurs d'un tournoi")
        print("8. Gérer les rondes")
        print("9. Afficher le classement final")
        print("10. Retour au menu principal")
        
        choix = input("Entrez votre choix : ")
        
        if choix == "1":
            # Créer un nouveau tournoi
            nom = input("Nom du tournoi : ")
            date_debut = input("Date de début (format YYYY-MM-DD) : ")
            date_fin = input("Date de fin (format YYYY-MM-DD) : ")
            nb_max_joueurs = int(input("Nombre maximum de joueurs : "))
            nb_rondes = int(input("Nombre de rondes : "))
            type_tournoi = input("Type de tournoi : ")
            
            nouveau_tournoi = tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
            if nouveau_tournoi:
                print(f"Le tournoi '{nom}' a été créé avec succès!")
        
        elif choix == "2":
            # Modifier un tournoi
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            if index_tournoi is not None:
                tournoi_vue.modifier_tournoi(index_tournoi)
        
        elif choix == "3":
            # Supprimer un tournoi
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            if index_tournoi is not None:
                tournoi_manager.supprimer_tournoi(index_tournoi)
        
        elif choix == "4":
            # Afficher la liste des tournois
            tournoi_vue.afficher_liste_tournois()
        
        elif choix == "5":
            # Afficher les détails d'un tournoi
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            if index_tournoi is not None:
                tournoi_vue.afficher_details_tournoi(index_tournoi)
        
        elif choix == '6':
            # Exemple d'appel pour ajouter des joueurs à un tournoi
            index_tournoi = tournoi_vue.saisir_tournoi()
            if index_tournoi is not None:
                tournoi_vue.saisir_joueurs_participants(index_tournoi - 1)
        elif choix == "7":
            # Supprimer des joueurs d'un tournoi
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            if index_tournoi is not None:
                tournoi_vue.supprimer_joueurs_participants(index_tournoi)
        
        elif choix == "8":
            # Gérer les rondes
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            if index_tournoi is not None:
                tournoi_vue.gerer_rondes(index_tournoi)
        
        elif choix == "9":
            # Afficher le classement final
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            if index_tournoi is not None:
                tournoi_vue.afficher_classement_final(index_tournoi)
        
        elif choix == "10":
            # Retour au menu principal
            break
        
        else:
            print("Choix invalide. Veuillez entrer un choix valide.")

if __name__ == "__main__":
    gestion_tournoi()
