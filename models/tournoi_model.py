import datetime
import json
import os
import random
from typing import List, Dict, Tuple, Optional
from models.joueur_model import Joueur

class Match:
    def __init__(self, joueur_blanc: Joueur, joueur_noir: Joueur, resultat: str = ""):
        self.joueur_blanc = joueur_blanc
        self.joueur_noir = joueur_noir
        self.resultat = resultat

    def saisir_resultat(self, resultat: str) -> None:
        if resultat in ["1-0", "0-1", "0.5-0.5"]:
            self.resultat = resultat
        else:
            raise ValueError("Le résultat doit être '1-0', '0-1' ou '0.5-0.5'.")

    def to_dict(self) -> Dict:
        return {
            "match": f"{self.joueur_blanc.nom} {self.joueur_blanc.prenom} - {self.joueur_noir.nom} {self.joueur_noir.prenom}",
            "score": self.resultat if self.resultat else "Non joué"
        }

    def __repr__(self) -> str:
        return f"{self.joueur_blanc.nom} vs {self.joueur_noir.nom}: {self.resultat}"

class Ronde:
    def __init__(self, numero: int, date: datetime.datetime = None, statut: str = "en cours"):
        self.numero = numero
        self.date = date if date else datetime.datetime.now()
        self.statut = statut
        self.matchs: List[Match] = []

    def ajouter_match(self, match: Match) -> None:
        self.matchs.append(match)

    def terminer_ronde(self) -> None:
        self.date_fin = datetime.datetime.now()

    def to_dict(self) -> Dict:
        return {
            "numero": self.numero,
            "date": self.date.isoformat(),
            "statut": self.statut,
            "matchs": [match.to_dict() for match in self.matchs],
            "classement_apres_ronde": self.obtenir_classement_ronde()
        }

    def appariement_ronde(self, joueurs: List[Joueur]) -> None:
        if len(joueurs) < 2:
            print("Nombre insuffisant de joueurs pour créer des paires.")
            return
        random.shuffle(joueurs)
        paires = [(joueurs[i], joueurs[i + 1]) for i in range(0, len(joueurs), 2) if i + 1 < len(joueurs)]
        self.matchs = [Match(pair[0], pair[1]) for pair in paires]

    def obtenir_resultats_ronde(self) -> None:
        print(f"Obtention des résultats pour la ronde {self.numero}.")
        for match in self.matchs:
            print(f"Match entre {match.joueur_blanc.nom} et {match.joueur_noir.nom}: {match.resultat}")

    def obtenir_classement_ronde(self) -> List[str]:
        classement = {match.joueur_blanc: 0 for match in self.matchs}
        classement.update({match.joueur_noir: 0 for match in self.matchs})
        for match in self.matchs:
            if match.resultat == "1-0":
                classement[match.joueur_blanc] += 1
            elif match.resultat == "0-1":
                classement[match.joueur_noir] += 1
            elif match.resultat == "0.5-0.5":
                classement[match.joueur_blanc] += 0.5
                classement[match.joueur_noir] += 0.5
        classement = sorted(classement.items(), key=lambda item: item[1], reverse=True)
        return [f"{i+1}. {joueur.nom} {joueur.prenom} : {points}" for i, (joueur, points) in enumerate(classement)]

class Tournoi:
    
    def __init__(self, index: int, nom: str, date_debut: datetime.date, date_fin: datetime.date,
                 nb_max_joueurs: int, nb_rondes: int, type_tournoi: str):
        self.index = index
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_max_joueurs = nb_max_joueurs
        self.nb_rondes = nb_rondes
        self.type_tournoi = type_tournoi
        self.joueurs: List[Joueur] = []
        self.rondes: List[Ronde] = []
        self.statut = "En attente"
        self.charger_joueurs()

    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "nom_tournoi": self.nom,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat(),
            "nb_rondes": int(self.nb_rondes),
            "nb_inscrits": len(self.joueurs),
            "nb_max_joueurs": int(self.nb_max_joueurs),
            "type_tournoi": self.type_tournoi,
            "statut": self.statut,
            "joueurs_inscrits": [joueur.to_dict() for joueur in self.joueurs],
            "rondes": [ronde.to_dict() for ronde in self.rondes]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Tournoi':
        tournoi = cls(
            data["index"],
            data["nom_tournoi"],
            datetime.date.fromisoformat(data["date_debut"]),
            datetime.date.fromisoformat(data["date_fin"]),
            data["nb_max_joueurs"],
            data["nb_rondes"],
            data["type_tournoi"]
        )
        tournoi.statut = data["statut"]
        # Charger les joueurs
        tournoi.charger_joueurs()
        # Charger les rondes
        for ronde_data in data.get("rondes", []):
            ronde = Ronde(
                numero=ronde_data["numero"],
                date=datetime.datetime.fromisoformat(ronde_data["date"]),
                statut=ronde_data["statut"]
            )
            for match_data in ronde_data.get("matchs", []):
                joueur_blanc = next((j for j in tournoi.joueurs if f"{j.nom} {j.prenom}" == match_data["match"].split(" - ")[0]), None)
                joueur_noir = next((j for j in tournoi.joueurs if f"{j.nom} {j.prenom}" == match_data["match"].split(" - ")[1]), None)
                if joueur_blanc and joueur_noir:
                    match = Match(joueur_blanc, joueur_noir, match_data["score"])
                    ronde.ajouter_match(match)
            tournoi.rondes.append(ronde)
        return tournoi

    def ajouter_joueur(self, joueur: Joueur) -> bool:
        if len(self.joueurs) < self.nb_max_joueurs and joueur not in self.joueurs:
            self.joueurs.append(joueur)
            self.sauvegarder_joueurs()
            self.sauvegarder_tournoi()
            return True
        return False


    def creer_ronde(self) -> Optional[Ronde]:
        if len(self.rondes) >= self.nb_rondes:
            print(f"Impossible de créer une nouvelle ronde. Le nombre maximum de rondes ({self.nb_rondes}) a déjà été atteint.")
            return None
        if len(self.joueurs) < 8:
            print(f"Impossible de créer une ronde. Il y a actuellement {len(self.joueurs)} joueurs inscrits, mais un minimum de 8 joueurs est requis.")
            return None
        nouvelle_ronde = Ronde(len(self.rondes) + 1, datetime.datetime.now())
        joueurs_disponibles = self.joueurs.copy()
        random.shuffle(joueurs_disponibles)
        while len(joueurs_disponibles) >= 2:
            joueur1 = joueurs_disponibles.pop()
            joueur2 = joueurs_disponibles.pop()
            match = Match(joueur1, joueur2)
            nouvelle_ronde.ajouter_match(match)
        if joueurs_disponibles:
            print(f"Le joueur {joueurs_disponibles[0].nom} {joueurs_disponibles[0].prenom} reçoit un bye pour cette ronde.")
        self.rondes.append(nouvelle_ronde)
        print(f"Ronde {nouvelle_ronde.numero} créée avec succès.")
        for match in nouvelle_ronde.matchs:
            print(f"{match.joueur_blanc.nom} {match.joueur_blanc.prenom} - {match.joueur_noir.nom} {match.joueur_noir.prenom}")
        self.sauvegarder_tournoi()
        return nouvelle_ronde

    def charger_joueurs(self) -> None:
        fichier_joueurs = f"data/tournaments/{self.nom.replace(' ', '_')}_joueurs.json"
        if os.path.exists(fichier_joueurs):
            with open(fichier_joueurs, 'r', encoding='utf-8') as file:
                joueurs_data = json.load(file)
                self.joueurs = [Joueur.from_dict(joueur_data) for joueur_data in joueurs_data]
        else:
            print(f"Fichier {fichier_joueurs} non trouvé.")

    def generer_paires(self):
        joueurs = set(self.joueurs)
        paires = []
        deja_apparies = set()
        while len(joueurs) >= 2:
            j1 = joueurs.pop()
            j2 = joueurs.pop()
            while (j1, j2) in deja_apparies or (j2, j1) in deja_apparies:
                joueurs.add(j1)
                j1 = joueurs.pop()
                joueurs.add(j2)
                j2 = joueurs.pop()
            paires.append((j1, j2))
            deja_apparies.add((j1, j2))
        return paires

    def jouer_ronde(self):
        if len(self.rondes) >= self.nb_rondes:
            print("Toutes les rondes ont été jouées.")
            return
        nouvelle_ronde = Ronde(len(self.rondes) + 1, datetime.datetime.now())
        paires = self.generer_paires()
        for j1, j2 in paires:
            match = Match(j1, j2)
            nouvelle_ronde.ajouter_match(match)
        self.rondes.append(nouvelle_ronde)
        print(f"Ronde {nouvelle_ronde.numero} créée avec succès.")
        for match in nouvelle_ronde.matchs:
            print(f"{match.joueur_blanc.nom} {match.joueur_blanc.prenom} - {match.joueur_noir.nom} {match.joueur_noir.prenom}")
        for match  in nouvelle_ronde.matchs:
            while True:
                resultat = input(f"Résultat du match {match.joueur_blanc.nom} {match.joueur_blanc.prenom} vs {match.joueur_noir.nom} {match.joueur_noir.prenom} (1-0, 0-1, 0.5-0.5) : ")
                try:
                    match.saisir_resultat(resultat)
                    # Mettre à jour les scores des joueurs
                    if resultat == "1-0":
                        match.joueur_blanc.score += 1
                    elif resultat == "0-1":
                        match.joueur_noir.score += 1
                    elif resultat == "0.5-0.5":
                        match.joueur_blanc.score += 0.5
                        match.joueur_noir.score += 0.5
                    break
                except ValueError as e:
                    print(e)
        nouvelle_ronde.statut = "terminée"
        print("\nClassement après la ronde :")
        for ligne in nouvelle_ronde.obtenir_classement_ronde():
            print(ligne)
        self.sauvegarder_tournoi()
        print(f"Ronde {nouvelle_ronde.numero} terminée et sauvegardée.")
    def saisir_resultats_ronde(self, numero_ronde: int) -> None:
        if numero_ronde <= 0 or numero_ronde > len(self.rondes):
            print(f"Numéro de ronde invalide. Il y a {len(self.rondes)} rondes dans ce tournoi.")
            return

        ronde = self.rondes[numero_ronde - 1]
        print(f"Saisie des résultats pour la ronde {numero_ronde}")

        for match in ronde.matchs:
            while True:
                resultat = input(f"Résultat du match {match.joueur_blanc.nom} vs {match.joueur_noir.nom} (1-0, 0-1, 0.5-0.5) : ")
                try:
                    match.saisir_resultat(resultat)
                    self.mettre_a_jour_scores_match(match, resultat)
                    break
                except ValueError as e:
                    print(e)

        ronde.statut = "terminée"
        self.mettre_a_jour_scores()
        self.sauvegarder_tournoi()
        print(f"Résultats de la ronde {numero_ronde} saisis et sauvegardés.")
    def mettre_a_jour_scores_match(self, match: Match, resultat: str) -> None:
        if resultat == "1-0":
            match.joueur_blanc.score += 1
        elif resultat == "0-1":
            match.joueur_noir.score += 1
        elif resultat == "0.5-0.5":
            match.joueur_blanc.score += 0.5
            match.joueur_noir.score += 0.5
    def mettre_a_jour_scores(self):
        for joueur in self.joueurs:
            joueur.score = 0
        for ronde in self.rondes:
            for match in ronde.matchs:
                if match.resultat == "1-0":
                    match.joueur_blanc.score += 1
                elif match.resultat == "0-1":
                    match.joueur_noir.score += 1
                elif match.resultat == "0.5-0.5":
                    match.joueur_blanc.score += 0.5
                    match.joueur_noir.score += 0.5

    def classement(self) -> List[tuple]:
        return sorted([(j, j.score) for j in self.joueurs], key=lambda x: x[1], reverse=True)

    def sauvegarder_tournoi(self) -> None:
        fichier_tournoi = f"data/tournaments/{self.nom.replace(' ', '_')}.json"
        with open(fichier_tournoi, "w", encoding='utf-8') as file:
            json.dump(self.to_dict(), file, indent=4, ensure_ascii=False)
    def demarrer_tournoi(self) -> None:
        if self.statut == "En attente":
            self.statut = "En cours"

    def terminer_tournoi(self) -> None:
        if self.statut == "En cours":
            self.statut = "Terminé"

    def sauvegarder_joueurs(self) -> None:
        fichier_joueurs = f"data/tournaments/{self.nom.replace(' ', '_')}_joueurs.json"
        joueurs_data = [joueur.to_dict() for joueur in self.joueurs]
        with open(fichier_joueurs, 'w', encoding='utf-8') as file:
            json.dump(joueurs_data, file, indent=4, ensure_ascii=False)
