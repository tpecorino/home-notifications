from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Entity(Base):
    __tablename__ = "entities"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(30))
    is_subscribed = Column("is_subscribed", Integer)

    def __repr__(self):
        return f"Entity(id={self.id!r}, name={self.name!r}, is_subscribed={self.is_subscribed!r})"
