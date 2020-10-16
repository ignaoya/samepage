from flask_restful import Resource
from models.event import EventModel

EVENT_ERROR = "Event not found"
SERVER_ERROR = "Internal Server Error"

class Event(Resource):
    @classmethod
    def get(cls, name: str):
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        return {"message": EVENT_ERROR}, 404

    @classmethod
    def post(cls, name: str):
        if EventModel.find_by_name(name):
            return {"message": f"An event with name '{name}' already exists."}, 400

        event = EventModel(name)
        try:
            event.save_to_db()
        except:
            return {"message": SERVER_ERROR}, 500

        return event.json(), 201

    @classmethod
    def delete(cls, name: str):
        event = EventModel.find_by_name(name)
        if event:
            event.delete_from_db()
        return {"message": "Event deleted."}


class EventList(Resource):
    @classmethod
    def get(cls):
        return {"events": [event.json() for event in EventModel.find_all()]}
