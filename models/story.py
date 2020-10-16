from typing import Dict, List

from db import db

class StoryModel(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    origin = db.Column(db.String(80))
    link = db.Column(db.String(255), unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('EventModel')

    def __init__(self, title: str, origin: str, link: str, event_id: int):
        self.title = title
        self.origin = origin
        self.link = link
        self.event_id = event_id

    def json(self) -> Dict:
        return {'title': self.title, 'origin': self.origin, 'link': self.link}

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(title=name).first()

    @classmethod
    def find_all(cls) ->List:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
