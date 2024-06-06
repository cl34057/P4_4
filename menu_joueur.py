from views.joueur_vue import JoueurVue


def gestion_joueur():
    from main_menu import main_menu # Importation locale pour éviter la circularité
    joueur_vue = JoueurVue(gestion_joueur)
    while True:
        joueur_vue.afficher_menu()
        choix = input("Entrez votre choix : ")

        if choix == "1":
            if joueur_vue.saisir_joueur() is True:
                continue
            elif len(joueur_vue.joueur_controller.joueur_manager.joueurs) >= joueur_vue.joueur_controller.joueur_manager.MAX_JOUEURS:
                print("Le nombre maximal de joueurs est déjà atteint.")
            else:
                joueur = joueur_vue.saisir_joueur()
                joueur_vue.joueur_controller.ajouter_joueur(joueur.nom, joueur.prenom, joueur.date_naissance, joueur.elo)
        elif choix == "2":
            joueur_vue.modifier_joueur()
        elif choix == "3":
            joueur_vue.supprimer_joueur()
        elif choix == "4":
            joueur_vue.afficher_liste_joueurs()
        elif choix == "5":
            joueur_vue.afficher_details_joueur()
        elif choix == "6": 
            print("retour au menu principal")
            main_menu()
            return
        else:
            print("Choix invalide. Veuillez réessayer.")
    return

if __name__ == "__main__":
    gestion_joueur()

