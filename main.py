import subscriber
import os
from dotenv import load_dotenv
from db import DBConnection
from gui import GUI
from get_home_entities import fetch_entities
from multiprocessing import Process

load_dotenv('./.env')


class HomeEventNotifier:
    def __init__(self):
        self.db = DBConnection()
        self.gui = GUI(self.db)
        self.home_entities = None
        self.access_token = os.environ["ACCESS_TOKEN"]
        self.rest_url = os.environ["REST_URL"]

    def start_processes(self):
        ui = self.gui.init()
        gui_process = Process(target=ui, daemon=True)
        subscriber_process = Process(target=subscriber.init, daemon=True)
        subscriber_process.start()
        gui_process.start()
        subscriber_process.join()
        gui_process.join()

    def fetch_entities(self):
        return self.db.fetch_entities()

    def run(self):
        home_entities = self.fetch_entities()

        if not home_entities:
            ha_entities = fetch_entities(self.rest_url, self.access_token)
            print(ha_entities)
            self.db.setup(ha_entities)

        self.start_processes()


if __name__ == '__main__':
    home_notification = HomeEventNotifier()
    home_notification.run()
