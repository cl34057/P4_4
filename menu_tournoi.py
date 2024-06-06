from views.tournoi_vue import TournoiVue
def gestion_tournoi():
    tournoi_vue = TournoiVue()
    
    while True:
        tournoi_vue.afficher_menu()
        choix = input("Entrez votre choix : ")
        if choix == "1":
            nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi = tournoi_vue.saisir_tournoi()
            if tournoi_vue.tournoi_controller.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
                print("Tournoi ajouté avec succès.")
            else:
                print("Erreur lors de l'ajout du tournoi.")
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
        elif choix == "3":
            index = tournoi_vue.saisir_index_tournoi()
            tournoi_vue.tournoi_controller.tournoi_manager.supprimer_tournoi(index - 1)
            print("Tournoi supprimé avec succès.")
        elif choix == "4":
            tournoi_vue.afficher_liste_tournois()
   
        elif choix == "5":
            print("1. Afficher les détails d'un tournoi")
            print("2. Créer une ronde")
            print("3. Afficher les résultats")
            print("4. Afficher le classement")
            choix_sous_menu = input("Sélectionnez une option : ")
            
            if choix_sous_menu  == "1":
                # Option a- détails d'un tournoi
                index = tournoi_vue.saisir_index_tournoi()
                tournoi = tournoi_vue.afficher_details_tournoi(index)
                if tournoi:
                    print("Détails du tournoi :")
                    # Afficher les détails du tournoi ici
                else:
                    print("Tournoi non trouvé.")
            elif choix_sous_menu == "2":
                # Option b- créer une ronde
                index = tournoi_vue.saisir_index_tournoi()
                tournoi = tournoi_vue.afficher_details_tournoi(index)
                if tournoi:
                    tournoi.creer_ronde()
                    print("Ronde créée avec succès.")
                else:
                    print("Tournoi non trouvé.")
            elif choix_sous_menu == "3":
                # Option 2- afficher les résultats
                index = tournoi_vue.saisir_index_tournoi()
                tournoi = tournoi_vue.afficher_details_tournoi(index)
                if tournoi:
                    for ronde in tournoi.rondes:
                        ronde.obtenir_resultats_ronde()
                else:
                    print("Tournoi non trouvé.")
            elif choix_sous_menu == "4":
                # Option 3- afficher le classement
                index = tournoi_vue.saisir_index_tournoi()
                tournoi = tournoi_vue.afficher_details_tournoi(index)
                if tournoi:
                    classement_final = tournoi.classement()
                    print("Classement final :")
                    for index, points in classement_final.items():
                        joueur = next(j for j in tournoi.joueurs if j.index == index)
                        print(f"{joueur.nom} {joueur.prenom}: {points} points")
                else:
                    print("Tournoi non trouvé.")
            else:
                print("Option invalide.")


        
        elif choix == "6":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    gestion_tournoi()
