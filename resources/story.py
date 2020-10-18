from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.story import StoryModel
from models.event import EventModel
from marshmallow import ValidationError
from schemas.story import StorySchema

STORY_ERROR = "Story not found"

story_schema = StorySchema()
story_list_schema = StorySchema(many=True)

class Story(Resource):
    @classmethod
    @jwt_required
    def get(cls, name: str):
        story = StoryModel.find_by_name(name)
        if story:
            return story_schema.dump(story)
        return {"message": STORY_ERROR}, 400

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        if StoryModel.find_by_name(name):
            return {"message": f"A story with name '{name}' already exists."}, 400
        else:
            story_json = request.get_json()
            story_json["title"] = name
            story = story_schema.load(story_json)

            try:
                story.save_to_db()
            except:
                return {"message": "An error occurred inserting story."}, 500

            return story_schema.dump(story), 201

    @classmethod
    def delete(cls, name: str):
        story = StoryModel.find_by_name(name)
        if story:
            story.delete_from_db()
        return {"message": "Story deleted."}

    @classmethod
    def put(cls, name: str):
        story_json = request.get_json()
        story = StoryModel.find_by_name(name)
        if story is None:
            story_json["title"] = name
            story = story_schema.load(story_json)
        else:
            story.origin = story_json["origin"]
            story.link = story_json["link"]
            story.event_id = story_json["event_id"]

        story.save_to_db()

        return story.json()


class StoryList(Resource):
    @classmethod
    def get(cls):
        return {"stories": story_list_schema.dump(StoryModel.find_all())}


class EventStoryList(Resource):
    @classmethod
    def get(cls, name: str):
        return {
            "stories": [story_schema.dump(story) for story in EventModel.find_by_name(name).stories]
        }, 200
