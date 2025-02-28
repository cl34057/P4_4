import datetime
from models.tournoi_manager import TournoiManager
from models.joueur_model import Joueur 
from typing import Optional
class TournoiController:
    def __init__(self):
        self.tournoi_manager = TournoiManager()

    def ajouter_tournoi(self, nom: str, date_debut: datetime.date, date_fin: datetime.date, nb_max_joueurs: int, nb_rondes: int, type_tournoi: str) -> bool:
        return self.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)

    def modifier_tournoi(self, index: int, nom: str, date_debut: datetime.date, date_fin: datetime.date, nb_max_joueurs: int, nb_rondes: int, type_tournoi: str) -> None:
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index)
        if tournoi:
            tournoi.nom = nom
            tournoi.date_debut = date_debut
            tournoi.date_fin = date_fin
            tournoi.nb_max_joueurs = nb_max_joueurs
            tournoi.nb_rondes = nb_rondes
            tournoi.type_tournoi = type_tournoi
            tournoi.sauvegarder_tournoi()
            print("Tournoi modifié avec succès.")
        else:
            print("Tournoi non trouvé.")

    def supprimer_tournoi(self, index: int) -> None:
        self.tournoi_manager.supprimer_tournoi(index)

    def ajouter_joueur_au_tournoi(self, index_tournoi: int, joueur: dict) -> bool:
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi:
            nouveau_joueur = Joueur(
                index=joueur['index'],
                nom=joueur['nom'],
                prenom=joueur['prenom'],
                date_naissance=datetime.datetime.strptime(joueur['date_naissance'], '%Y-%m-%d').date(),
                elo=joueur['elo']
            )
            if tournoi.ajouter_joueur(nouveau_joueur):
                tournoi.sauvegarder_tournoi()
                return True
        return False

    def supprimer_joueur_du_tournoi(self, index_tournoi: int, joueur: Joueur) -> bool:
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi:
            tournoi.joueurs.remove(joueur)
            tournoi.sauvegarder_joueurs()
            tournoi.sauvegarder_tournoi()
            return True
        return False
    def creer_ronde(self, index_tournoi):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi:
            tournoi.creer_ronde()
            self.tournoi_manager.sauvegarder_tournois()
            print("Ronde créée avec succès.")
        else:
            print("Tournoi non trouvé.")

    def modifier_ronde(self, index_tournoi, ronde_numero):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi and 0 < ronde_numero <= len(tournoi.rondes):
            ronde = tournoi.rondes[ronde_numero - 1]
            print(f"Modification de la ronde {ronde.numero}")

            for i, match in enumerate(ronde.matchs):
                print(f"Match {i + 1}: {match.joueur_blanc.nom} vs {match.joueur_noir.nom} - Résultat actuel: {match.resultat}")
                resultat = input(f"Entrez le nouveau résultat pour {match.joueur_blanc.nom} vs {match.joueur_noir.nom} (ex: 1-0, 0.5-0.5) ou laissez vide pour conserver l'actuel: ")
                if resultat:
                    match.saisir_resultat(resultat)

            self.tournoi_manager.sauvegarder_tournois()
            print("Ronde modifiée avec succès.")
        else:
            print("Numéro de ronde invalide.")

    def supprimer_ronde(self, index_tournoi, ronde_numero):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi and 0 < ronde_numero <= len(tournoi.rondes):
            tournoi.rondes.pop(ronde_numero - 1)
            self.tournoi_manager.sauvegarder_tournois()
            print("Ronde supprimée avec succès.")
        else:
            print("Numéro de ronde invalide.")

    def afficher_resultats_ronde(self, index_tournoi, ronde_numero):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi and 0 < ronde_numero <= len(tournoi.rondes):
            return tournoi.rondes[ronde_numero - 1]
        return None

    def afficher_classement_final(self, index_tournoi):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        if tournoi:
            scores = {}
            for ronde in tournoi.rondes:
                for match in ronde.matchs:
                    joueur_blanc = match.joueur_blanc
                    joueur_noir = match.joueur_noir
                    resultat = match.resultat

                    if joueur_blanc not in scores:
                        scores[joueur_blanc] = 0
                    if joueur_noir not in scores:
                        scores[joueur_noir] = 0

                    if resultat == "1-0":
                        scores[joueur_blanc] += 1
                    elif resultat == "0-1":
                        scores[joueur_noir] += 1
                    elif resultat == "0.5-0.5":
                        scores[joueur_blanc] += 0.5
                        scores[joueur_noir] += 0.5

            classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            return classement
        else:
            print("Tournoi non trouvé")
            return None

    def trouver_tournoi_par_index(self, index):
        return self.tournoi_manager.trouver_tournoi_par_index(index)

    def appariement_ronde(self, index_tournoi):
        self.tournoi_manager.appariement_ronde(index_tournoi)

    def obtenir_resultats_ronde(self, index_tournoi):
        return self.tournoi_manager.obtenir_resultats_ronde(index_tournoi)

    def obtenir_classement_ronde(self, index_tournoi):
        return self.tournoi_manager.obtenir_classement_ronde(index_tournoi)
