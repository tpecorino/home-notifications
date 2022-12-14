from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect
from sqlalchemy.orm import Session
from models.Entity import Entity
from pathlib import Path


class DBConnection:
    db_path = Path("{}\sqlite\home_automation.db".format(str(Path.home())))

    engine = create_engine("sqlite:///{}".format(db_path),
                           echo=True, future=True, connect_args={'check_same_thread': False})
    session = None

    if session is None:
        print("Create Session")
        session = Session(engine)

    table_name = "entities"

    def __init__(self):
        table_exists = inspect(self.engine).has_table(self.table_name)

        if not self.db_path.is_file():
            print("Database not found. Creating one.")
            self.db_path.parent.mkdir(exist_ok=True, parents=True)

        if not table_exists:
            self.create_table()

    def create_table(self):
        metadata = MetaData(self.engine)
        Table(self.table_name, metadata,
              Column('id', Integer, primary_key=True, nullable=False, unique=True, autoincrement=True),
              Column('name', String),
              Column('is_subscribed', Integer, nullable=False))
        metadata.create_all()

    def fetch_entities(self):
        return self.session.query(Entity).all()

    def fetch_entity_by_name(self, name):
        return self.session.query(Entity).filter(Entity.name == name).first()

    def fetch_entity_by_is_subscribed(self):
        return self.session.query(Entity.name).filter(Entity.is_subscribed == 1).all()

    def update_entity(self, entity_id, is_subscribed):
        self.session.query(Entity).filter(Entity.name == entity_id).update({'is_subscribed': is_subscribed})
        self.session.commit()

    def count(self):
        return self.session.query(Entity).count()

    def setup(self, items):
        entities_list = []

        print("Inserting data.")
        for entity in items:
            new_entity = Entity(
                name=entity,
                is_subscribed=0
            )

            entities_list.append(new_entity)

            print("Adding items to database.")
            self.session.add_all(entities_list)
            self.session.commit()
