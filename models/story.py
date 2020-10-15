from db import db

class StoryModel(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    origin = db.Column(db.String(80))
    link = db.Column(db.String(255))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('EventModel')

    def __init__(self, title, origin, link, event_id):
        self.title = title
        self.origin = origin
        self.link = link
        self.event_id = event_id

    def json(self):
        return {'title': self.title, 'origin': self.origin, 'link': self.link}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(title=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
