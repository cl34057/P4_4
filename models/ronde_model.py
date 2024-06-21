from models.match_model import Match

class Ronde:
    def __init__(self, nom, matchs=None):
        self.nom = nom
        self.matchs = matchs if matchs else []

    def ajouter_match(self, match):
        self.matchs.append(match)

    def generer_donnees_json(self):
        return {
            "nom": self.nom,
            "matchs": [match.generer_donnees_json() for match in self.matchs],
            "classement": self.generer_classement()
        }

    def generer_classement(self):
        classement = []
        points = {}

        for match in self.matchs:
            if match.resultat:
                if match.resultat == "blanc":
                    points[match.joueur1.nom] = points.get(match.joueur1.nom, 0) + 1
                elif match.resultat == "noir":
                    points[match.joueur2.nom] = points.get(match.joueur2.nom, 0) + 1
                elif match.resultat == "nul":
                    points[match.joueur1.nom] = points.get(match.joueur1.nom, 0) + 0.5
                    points[match.joueur2.nom] = points.get(match.joueur2.nom, 0) + 0.5

        for joueur, point in points.items():
            classement.append({"nom": joueur, "points": point})

        classement.sort(key=lambda x: x["points"], reverse=True)
        return classement
