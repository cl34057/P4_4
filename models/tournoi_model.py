import json
import os
import random
import datetime
from typing import List
from models.joueur_model import Joueur

def date_encoder(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

class Tournoi:
    def __init__(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi, joueurs=None):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_max_joueurs = nb_max_joueurs
        self.nb_rondes = nb_rondes
        self.type_tournoi = type_tournoi
        self.joueurs = joueurs if joueurs is not None else []
        self.nombre_inscrits = len(self.joueurs)
        self.rondes = []

    def generer_donnees_json(self):
        data = {
            "nom": self.nom,
            "date_debut": str(self.date_debut),
            "date_fin": str(self.date_fin),
            "nb_max_joueurs": self.nb_max_joueurs,
            "nombre_joueurs_inscrits": self.nombre_inscrits,
            "nb_rondes": self.nb_rondes,
            "type_tournoi": self.type_tournoi,
            "rondes": [ronde.generer_donnees_json() for ronde in self.rondes]
        }
        return data

    def creer_fichier_json(self):
        filename = "data/tournaments.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = json.load(file)
        else:
            data = {}
        
        data[self.nom] = self.generer_donnees_json()
        
        with open(filename, "w") as file:
            json.dump(data, file, indent=4, default=date_encoder)

    def creer_ronde(self):
        if self.date_fin < datetime.datetime.now().date():
            print("Impossible de créer un nouveau tour. Le tournoi est terminé.")
            return
        
        if len(self.rondes) >= self.nb_rondes:
            print("Impossible de créer un nouveau tour. Le nombre maximum de tours est atteint.")
            return

        nouvelle_ronde = Ronde(len(self.rondes) + 1, datetime.datetime.now(), "en cours")
        self.rondes.append(nouvelle_ronde)
        self.mise_a_jour_fichier_json()

    def ajouter_ronde(self, ronde):
        self.rondes.append(ronde)

    def mise_a_jour_fichier_json(self):
        if not os.path.exists("data/tournaments"):
            os.makedirs("data/tournaments")
        self.creer_fichier_json()

    def ajouter_joueur_au_tournoi(self, joueurs):
        self.joueurs.extend(joueurs)
        self.nombre_inscrits = len(self.joueurs)  # Mettre à jour le nombre d'inscrits
        self.mise_a_jour_fichier_json()

    def supprimer_joueur_du_tournoi(self, joueur):
        if joueur in self.joueurs:
            self.joueurs.remove(joueur)
            self.nombre_inscrits = len(self.joueurs)  # Mettre à jour le nombre d'inscrits
            self.mise_a_jour_fichier_json()
            print(f"Le joueur {joueur.nom} a été supprimé du tournoi {self.nom}.")
        else:
            print(f"Le joueur {joueur.nom} n'est pas inscrit dans ce tournoi.")

    def charger_joueurs(self):
        filepath = f"data/tournaments/{self.nom}_joueurs.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                joueurs_data = json.load(file)
                self.joueurs = [Joueur(**data) for data in joueurs_data]

    def sauvegarder_joueurs(self):
        filepath = f"data/tournaments/{self.nom}_joueurs.json"
        with open(filepath, "w") as file:
            json.dump([joueur.__dict__ for joueur in self.joueurs], file, indent=4, default=date_encoder)

    def classement(self):
        classement = {joueur.index: 0 for joueur in self.joueurs}
        for ronde in self.rondes:
            for match in ronde.matchs:
                if match.resultat == "blanc":
                    classement[match.joueur_blanc.index] += 1
                elif match.resultat == "noir":
                    classement[match.joueur_noir.index] += 1
                elif match.resultat == "nul":
                    classement[match.joueur_blanc.index] += 0.5
                    classement[match.joueur_noir.index] += 0.5
        classement = sorted(classement.items(), key=lambda item: item[1], reverse=True)
        return classement

class Match:
    def __init__(self, joueur_blanc, joueur_noir, resultat=""):
        self.joueur_blanc = joueur_blanc
        self.joueur_noir = joueur_noir
        self.resultat = resultat

    def saisir_resultat(self, resultat):
        if resultat in ["blanc", "noir", "nul"]:
            self.resultat = resultat
        else:
            raise ValueError("Le résultat doit être 'blanc', 'noir' ou 'nul'.")

    def generer_donnees_json(self):
        return {
            "joueur_blanc": self.joueur_blanc.index,
            "joueur_noir": self.joueur_noir.index,
            "resultat": self.resultat
        }

    def __repr__(self):
        return f"{self.joueur_blanc.nom} vs {self.joueur_noir.nom}: {self.resultat}"

class Ronde:
    def __init__(self, numero, date, statut):
        self.numero = numero
        self.date = date
        self.statut = statut
        self.matchs = []

    def ajouter_match(self, match):
        self.matchs.append(match)

    def generer_donnees_json(self):
        return {
            "numero": self.numero,
            "date": self.date.isoformat(),
            "statut": self.statut,
            "matchs": [match.generer_donnees_json() for match in self.matchs]
        }

    def appariement_ronde(self, joueurs):
        if len(joueurs) < 2:
            print("Nombre insuffisant de joueurs pour créer des paires.")
            return

        random.shuffle(joueurs)

        paires = []
        for i in range(0, len(joueurs), 2):
            if i + 1 < len(joueurs):
                paires.append((joueurs[i], joueurs[i + 1]))

        self.matchs = [Match(pair[0], pair[1]) for pair in paires]

    def obtenir_resultats_ronde(self):
        print(f"Obtention des résultats pour la ronde {self.numero}.")
        for match in self.matchs:
            print(f"Match entre {match.joueur_blanc.nom} et {match.joueur_noir.nom}: {match.resultat}")

    def obtenir_classement_ronde(self):
        print(f"Classement pour la ronde {self.numero}.")
        classement = sorted(self.matchs, key=lambda x: x.resultat, reverse=True)
        for i, match in enumerate(classement):
            print(f"{i+1}. {match.joueur_blanc.nom} vs {match.joueur_noir.nom}: {match.resultat}")

class TournoiManager:
    MAX_TOURNOIS = 15

    def __init__(self):
        self.tournois = []
        self.charger_tournois()

    def charger_tournois(self):
        FICHIER_JSON = "data/tournaments.json"
        if os.path.exists(FICHIER_JSON):
            with open(FICHIER_JSON, "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    for tournoi_data in data:
                        tournoi = Tournoi(
                            tournoi_data["nom"],
                            datetime.datetime.fromisoformat(tournoi_data["date_debut"]).date(),
                            datetime.datetime.fromisoformat(tournoi_data["date_fin"]).date(),
                            tournoi_data["nb_max_joueurs"],
                            tournoi_data["nb_rondes"],
                            tournoi_data["type_tournoi"]
                        )
                        self.tournois.append(tournoi)
                elif isinstance(data, dict):
                    for tournoi_data in data.values():
                        tournoi = Tournoi(
                            tournoi_data["nom"],
                            datetime.datetime.fromisoformat(tournoi_data["date_debut"]).date(),
                            datetime.datetime.fromisoformat(tournoi_data["date_fin"]).date(),
                            tournoi_data["nb_max_joueurs"],
                            tournoi_data["nb_rondes"],
                            tournoi_data["type_tournoi"]
                        )
                        self.tournois.append(tournoi)
                else:
                    print("Format de données non pris en charge dans le fichier JSON.")
        else:
            print(f"Le fichier {FICHIER_JSON} n'existe pas.")

    def sauvegarder_tournois(self):
        filename = "data/tournaments.json"
        data = {tournoi.nom: tournoi.generer_donnees_json() for tournoi in self.tournois}
        with open(filename, "w") as file:
            json.dump(data, file, indent=4, default=date_encoder)

    def ajouter_tournoi(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
        tournoi = Tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
        self.tournois.append(tournoi)
        self.sauvegarder_tournois()
        return tournoi

    def sauvegarder_joueurs(self, tournoi):
        filepath = f"data/tournaments/{tournoi.nom}_joueurs.json"
        joueurs_data = [joueur.__dict__ for joueur in tournoi.joueurs]
        with open(filepath, "w") as file:
            json.dump(joueurs_data, file, indent=4, default=date_encoder)

    def modifier_tournoi(self, index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
        tournoi = self.tournois[index]
        tournoi.nom = nom
        tournoi.date_debut = date_debut
        tournoi.date_fin = date_fin
        tournoi.nb_max_joueurs = nb_max_joueurs
        tournoi.nb_rondes = nb_rondes
        tournoi.type_tournoi = type_tournoi
        self.sauvegarder_tournois()

    def supprimer_tournoi(self, index):
        del self.tournois[index]
        self.sauvegarder_tournois()

    def trouver_tournoi_par_index(self, index):
        if 0 <= index < len(self.tournois):
            return self.tournois[index]
        return None

    def trouver_tournoi_par_nom(self, nom):
        for tournoi in self.tournois:
            if tournoi.nom == nom:
                return tournoi
        return None

    def charger_joueurs_par_index(self, joueurs_index):
        joueurs = []
        fichier_joueurs = "data/joueur.json"
        
        if os.path.exists(fichier_joueurs):
            with open(fichier_joueurs, "r") as file:
                all_players = json.load(file)
                
                # Créer un dictionnaire pour un accès rapide par index
                players_dict = {player['index']: player for player in all_players}
                
                for index in joueurs_index:
                    if index in players_dict:
                        player_data = players_dict[index]
                        try:
                            date_naissance = datetime.datetime.strptime(player_data['date_naissance'], '%Y-%m-%d').date()
                        except ValueError:
                            print(f"La date de naissance pour le joueur avec l'index {index} n'est pas au bon format.")
                            continue
                        
                        joueur = Joueur(
                            index=index,
                            nom=player_data['nom'],
                            prenom=player_data['prenom'],
                            date_naissance=date_naissance,
                            elo=player_data['elo']
                        )
                        joueurs.append(joueur)
                    else:
                        print(f"Les données pour le joueur avec l'index {index} n'ont pas été trouvées.")
        else:
            print("Le fichier des joueurs n'existe pas.")
        
        return joueurs
#*******************************tester et démontrer le fonctionnement du gestionnaire de tournoi.********************************
if __name__ == "__main__":
    # Initialisation du Gestionnaire de Tournoi 
    manager = TournoiManager()
    manager.charger_tournois()
    #Ajout d'un Nouveau Tournoi
    tournoi = manager.ajouter_tournoi("Tournoi test", datetime.date(2024, 6, 1), datetime.date(2024, 6, 10), 16, 4, "round-robin")
    manager.sauvegarder_tournois()

    # Ajout de joueurs fictifs pour les tests
    joueurs = [Joueur(index=i, nom=f"Nom{i}", prenom=f"Prenom{i}", date_naissance=datetime.date(1990, 1, 1), elo=1500) for i in range(1, 17)]
    tournoi.ajouter_joueur_au_tournoi(joueurs)
    tournoi.sauvegarder_joueurs()

    # Création et gestion des rondes
    for i in range(tournoi.nb_rondes):
        tournoi.creer_ronde()
        ronde = tournoi.rondes[-1]
        ronde.appariement_ronde(tournoi.joueurs)
        for match in ronde.matchs:
            match.saisir_resultat(random.choice(["blanc", "noir", "nul"]))
        ronde.statut = "terminée"
        tournoi.mise_a_jour_fichier_json()

    # Affichage des résultats
    for ronde in tournoi.rondes:
        ronde.obtenir_resultats_ronde()

    # Affichage du classement final
    classement_final = tournoi.classement()
    print("Classement final :")
    for index, points in classement_final:
        joueur = next(j for j in tournoi.joueurs if j.index == index)
        print(f"{joueur.nom} {joueur.prenom}: {points} points")