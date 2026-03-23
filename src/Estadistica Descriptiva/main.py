import sys
import os

# Add src package root to path so imports like "from models.table import Table" work
sys.path.insert(0, os.path.dirname(__file__))

from controllers.app_controller import AppController
from views.main_window import MainWindow


def main():
    controller = AppController()
    window = MainWindow("Estadística Descriptiva", controller)
    window.run()


if __name__ == "__main__":
    main()
