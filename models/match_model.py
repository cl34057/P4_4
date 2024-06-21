from models.joueur_model import Joueur

class Match:
    def __init__(self, joueur1, joueur2, resultat=None):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.resultat = resultat

    def generer_donnees_json(self):
        return {
            "joueur1": {"nom": self.joueur1.nom, "prenom": self.joueur1.prenom},
            "joueur2": {"nom": self.joueur2.nom, "prenom": self.joueur2.prenom},
            "resultat": self.resultat
        }

    def saisir_resultat(self, resultat: str) -> None:
        if resultat in ["blanc", "noir", "nul"]:
            self.resultat = resultat
        else:
            raise ValueError("Le résultat doit être 'blanc', 'noir' ou 'nul'.")

    def __repr__(self):
        return f"{self.joueur1.nom} vs {self.joueur2.nom}: {self.resultat}"
