from typing import List

from db import db

class StoryModel(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    origin = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(255), nullable=False, unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    event = db.relationship("EventModel")
    left = db.Column(db.Integer, nullable=False, default=0)
    right = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def find_by_name(cls, name: str) -> "StoryModel":
        return cls.query.filter_by(title=name).first()

    @classmethod
    def find_all(cls) -> List["StoryModel"]:
        return cls.query.all()

    def up_vote_left(self):
        self.left += 1

    def up_vote_right(self):
        self.right += 1


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
