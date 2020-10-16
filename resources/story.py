from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.story import StoryModel
from models.event import EventModel

BLANK_ERROR = "{} cannot be blank."
STORY_ERROR = "Story not found"

class Story(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "origin", type=str, required=True, help=BLANK_ERROR.format("origin")
    )
    parser.add_argument(
        "link", type=str, required=True, help=BLANK_ERROR.format("link")
    )
    parser.add_argument(
        "event_id", type=int, required=True, help=BLANK_ERROR.format("event_id")
    )

    def get(self, name: str):
        story = StoryModel.find_by_name(name)
        if story:
            return story.json()
        return {"message": STORY_ERROR}, 400

    def post(self, name: str):
        if StoryModel.find_by_name(name):
            return {"message": f"A story with name '{name}' already exists."}, 400
        else:
            data = Story.parser.parse_args()
            story = StoryModel(name, **data)
            try:
                story.save_to_db()
            except:
                return {"message": "An error occurred inserting story."}, 500
            return story.json(), 201

    def delete(self, name: str):
        story = StoryModel.find_by_name(name)
        if story:
            story.delete_from_db()
        return {"message": "Story deleted."}

    def put(self, name: str):
        data = Story.parser.parse_args()
        story = StoryModel.find_by_name(name)
        if story is None:
            story = StoryModel(name, **data)
        else:
            story.origin = data["origin"]
            story.link = data["link"]
            story.event_id = data["event_id"]

        story.save_to_db()

        return story.json()


class StoryList(Resource):
    def get(self):
        return {"stories": [story.json() for story in StoryModel.find_all()]}


class EventStoryList(Resource):
    def get(self, name: str):
        # return {'stories': [story.json() for story in StoryModel.query.all()]}
        return {
            "stories": [story.json() for story in EventModel.find_by_name(name).stories]
        }
