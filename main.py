from controllers.tournoi_controller import TournoiController
from models.tournoi_model import TournoiManager
from views.tournoi_vue import TournoiVue

def main():
    tournoi_manager = TournoiManager()
    tournoi_controller = TournoiController(tournoi_manager)
    tournoi_vue = TournoiVue(tournoi_controller)
    tournoi_vue.run()

if __name__ == "__main__":
    main()
