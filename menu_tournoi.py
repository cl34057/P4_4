from views.tournoi_vue import TournoiVue

def gestion_tournoi(tournoi_vue: TournoiVue):
    while True:
        tournoi_vue.afficher_menu()
        choix = input("Entrez votre choix : ")
        # 1-Création Nouveau Tournoi
        if choix == "1":
            nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi = tournoi_vue.saisir_tournoi()
            if tournoi_vue.tournoi_controller.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
                print("Tournoi ajouté avec succès.")
            else:
                print("Erreur lors de l'ajout du tournoi.")
        # 2- Modifier tournoi
        elif choix == "2":
             while True:
                print("===== Menu Modifier tournoi =====")
                print("a. Modification d'un tournoi")
                print("b. Ajouter un joueur au tournoi")
                print("c. Supprimer un joueur du tournoi")
                print("d. Retour au menu principal")
                sous_choix = input("Entrez votre choix : ")
                
                if sous_choix == "a":
                    tournoi_vue.modifier_tournoi()
                elif sous_choix == "b":
                    index_tournoi = tournoi_vue.saisir_index_tournoi()
                    tournoi_vue.saisir_joueurs_participants(index_tournoi)
                    print("Joueur ajouté au tournoi avec succès.")
                elif sous_choix == "c":
                    index_tournoi = tournoi_vue.saisir_index_tournoi()
                    tournoi_vue.supprimer_joueur_tournoi(index_tournoi)
                    print("Joueur supprimé du tournoi avec succès.")
                elif sous_choix == "d":
                    break
                else:
                    print("Choix invalide. Veuillez réessayer.")

        # 3- Supprimer tournoi
        elif choix == "3":
                index_tournoi = tournoi_vue.saisir_index_tournoi()
                if tournoi_vue.tournoi_controller.tournoi_manager.supprimer_tournoi(index_tournoi):
                        print("Tournoi supprimé avec succès.")
                else:
                        print("Erreur lors de la suppression du tournoi.")

        # 4- Afficher liste des tournois
        elif choix == "4":
            tournoi_vue.afficher_liste_tournois()
        # 5- Afficher details d'un tournoi
        elif choix == "5":
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            tournoi = tournoi_vue.afficher_details_tournoi(index_tournoi)
            if tournoi:
                while True:
                    print("1. Afficher les détails d'un tournoi")
                    print("2. Créer une ronde")
                    print("3. Jouer une ronde")
                    print("4. Saisir les résultats d'une ronde")
                    print("5. Afficher le classement")
                    print("6. Retour")
                    option = input("Sélectionnez une option : ")
                    if option == "1":
                        tournoi_vue.afficher_details_tournoi(index_tournoi)
                    elif option == "2":
                        tournoi.creer_ronde()
                        print("Ronde créée avec succès.")
                    elif option == "3":
                        tournoi.jouer_ronde()
                    elif option == "4":
                        numero_ronde = int(input("Entrez le numéro de la ronde : "))
                        tournoi.saisir_resultats_ronde(numero_ronde)
                    elif option == "5":
                        print("Classement :")
                        for ligne in tournoi.classement():
                            print(f"{ligne[0].nom} {ligne[0].prenom} : {ligne[1]} points")
                    elif option == "6":
                        break
                    else:
                        print("Option invalide.")
        # 6- Quitter
        elif choix == "6":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    from controllers.tournoi_controller import TournoiController
    from models.joueur_model import JoueurManager
    
    tournoi_controller = TournoiController()
    joueur_manager = JoueurManager()
    tournoi_vue = TournoiVue(tournoi_controller, joueur_manager)
    gestion_tournoi(tournoi_vue)