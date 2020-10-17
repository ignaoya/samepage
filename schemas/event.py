from ma import ma
from models.event import EventModel
from models.story import StoryModel
from schemas.story import StorySchema


class EventSchema(ma.SQLAlchemyAutoSchema):
    stories = ma.Nested(StorySchema, many=True)
    class Meta:
        model = EventModel
        load_instance = True
        dump_only = ("id",)
        include_fk = True
