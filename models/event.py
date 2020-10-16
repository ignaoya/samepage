from typing import Dict, List, Union
from db import db
from models.story import StoryJSON

EventJSON = Dict[str, Union[int, str, List[StoryJSON]]]


class EventModel(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    stories = db.relationship("StoryModel", lazy=True)

    def __init__(self, name: str):
        self.name = name

    def json(self) -> EventJSON:
        return {
            "id": self.id,
            "name": self.name,
            "stories": [story.json() for story in self.stories],
        }

    @classmethod
    def find_by_name(cls, name: str) -> "EventModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["EventModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
