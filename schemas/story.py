from ma import ma
from models.story import StoryModel
from models.event import EventModel


class StorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoryModel
        load_instance = True
        load_only = ("event",)
        dump_only = ("id",)
        include_fk = True
