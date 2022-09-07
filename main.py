import subscriber
import gui
import os
from dotenv import load_dotenv
from db import DBConnection
from fetch_entities import fetch_entities
from multiprocessing import Process

load_dotenv('./.env')

access_token = os.environ["ACCESS_TOKEN"]
url = os.environ["REST_URL"]

db = DBConnection()

home_entities = db.fetch_entities()

if not home_entities:
    ha_entities = fetch_entities(url, access_token)
    print(ha_entities)
    db.setup(ha_entities)

if __name__ == '__main__':
    two = Process(target=subscriber.init, daemon=True)

    ui = gui.init
    one = Process(target=ui, daemon=True)
    two.start()
    one.start()
    two.join()
    one.join()

