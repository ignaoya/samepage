from flask_restful import Resource
from models.event import EventModel

class Event(Resource):
    def get(self, name):
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        return {'message': 'Event not found'}, 404

    def post(self, name):
        if EventModel.find_by_name(name):
            return {'message': f"An event with name '{name}' already exists."}, 400

        event = EventModel(name)
        try:
            event.save_to_db()
        except:
            return {'message': 'Internal Server Error'}, 500

        return event.json(), 201

    def delete(self, name):
        event = EventModel.find_by_name(name)
        if event:
            event.delete_from_db()
        return {'message': 'Event deleted.'}


class EventList(Resource):
    def get(self):
        return {'events': [event.json() for event in EventModel.find_all()]}

