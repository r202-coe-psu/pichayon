import mongoengine as me
import datetime


class Rrule(me.EmbeddedDocument):
    days = me.ListField(me.IntField())
    start_time = me.ListField(me.IntField())
    end_time = me.ListField(me.IntField())


class GroupAuthorization(me.Document):
    meta = {"collection": "group_authorizations"}

    door_group = me.ReferenceField("DoorGroup", dbref=True, required=True)
    user_group = me.ReferenceField("UserGroup", dbref=True, required=True)

    granter = me.ReferenceField("User", dbref=True)
    rrule = me.EmbeddedDocumentField("Rrule")

    started_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    expired_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    status = me.StringField(required=True, default="active")
