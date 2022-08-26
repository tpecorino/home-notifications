from dotenv import load_dotenv
import os
from db import DBConnection
import gui

load_dotenv('./.env')

access_token = os.environ["ACCESS_TOKEN"]
url = os.environ["REST_URL"]

db = DBConnection()

home_entities = db.fetch_entities()

gui.init(home_entities)
