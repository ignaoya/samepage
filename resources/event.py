from flask_restful import Resource
from models.event import EventModel

EVENT_ERROR = "Event not found"
SERVER_ERROR = "Internal Server Error"

class Event(Resource):
    def get(self, name: str):
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        return {"message": EVENT_ERROR}, 404

    def post(self, name: str):
        if EventModel.find_by_name(name):
            return {"message": f"An event with name '{name}' already exists."}, 400

        event = EventModel(name)
        try:
            event.save_to_db()
        except:
            return {"message": SERVER_ERROR}, 500

        return event.json(), 201

    def delete(self, name: str):
        event = EventModel.find_by_name(name)
        if event:
            event.delete_from_db()
        return {"message": "Event deleted."}


class EventList(Resource):
    def get(self):
        return {"events": [event.json() for event in EventModel.find_all()]}
