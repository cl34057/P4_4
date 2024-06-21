import os
import json
from models.tournoi_model import TournoiManager, Tournoi

class TournoiController:
    def __init__(self, tournoi_manager: TournoiManager):
        self.tournoi_manager = tournoi_manager

    def ajouter_tournoi(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
        return self.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)

    def modifier_tournoi(self, index, nom=None, date_debut=None, date_fin=None, nb_max_joueurs=None, nb_rondes=None, type_tournoi=None):
        if index < len(self.tournoi_manager.tournois):
            self.tournoi_manager.modifier_tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
            return True
        else:
            return False

    def supprimer_tournoi(self, index):
        self.tournoi_manager.supprimer_tournoi(index)

    def sauvegarder_tournoi(self, tournoi):
        self.tournoi_manager.sauvegarder_tournoi(tournoi)

    def trouver_tournoi_par_index(self, index):
        return self.tournoi_manager.trouver_tournoi_par_index(index)

    def afficher_tous_les_tournois(self):
        return self.tournoi_manager.tournois

    def ajouter_joueur_au_tournoi(self, tournoi_index, joueurs_selectionnes):
        self.tournoi_manager.ajouter_joueur_au_tournoi(tournoi_index, joueurs_selectionnes)

    def supprimer_joueur_du_tournoi(self, tournoi_index, joueur):
        self.tournoi_manager.supprimer_joueur_du_tournoi(tournoi_index, joueur)

    def creer_ronde(self, index_tournoi):
        self.tournoi_manager.creer_ronde(index_tournoi)

    def modifier_ronde(self, index_tournoi, ronde_numero):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi and 0 < ronde_numero <= len(tournoi.rondes):
            ronde = tournoi.rondes[ronde_numero - 1]
            print(f"Modification de la {ronde.nom}")

            for i, match in enumerate(ronde.matchs):
                print(f"Match {i + 1}: {match.joueur1.nom} vs {match.joueur2.nom} - Résultat actuel: {match.resultat}")
                resultat = input(f"Entrez le nouveau résultat pour {match.joueur1.nom} vs {match.joueur2.nom} (ex: 1-0, 0.5-0.5) ou laissez vide pour conserver l'actuel: ")
                if resultat:
                    match.saisir_resultat(resultat)

            self.tournoi_manager.sauvegarder_tournois()
            print("Ronde modifiée avec succès.")
        else:
            print("Numéro de ronde invalide.")

    def supprimer_ronde(self, index_tournoi, ronde_numero):
        self.tournoi_manager.supprimer_ronde(index_tournoi, ronde_numero)

    def appariement_ronde(self, index_tournoi):
        self.tournoi_manager.appariement_ronde(index_tournoi)

    def afficher_resultats_ronde(self, index_tournoi, ronde_numero):
        return self.tournoi_manager.afficher_resultats_ronde(index_tournoi, ronde_numero)

    def obtenir_classement_ronde(self, index_tournoi):
        return self.tournoi_manager.obtenir_classement_ronde(index_tournoi)

    def afficher_classement_final(self, index_tournoi):
        return self.tournoi_manager.afficher_classement_final(index_tournoi)

    def obtenir_classement_final(self, index_tournoi):
        return self.tournoi_manager.obtenir_classement_final(index_tournoi)
