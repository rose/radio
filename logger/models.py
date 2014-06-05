from django.db.models import Model, CharField, DateField, TimeField, ForeignKey
from durationfield.db.models.fields.duration import DurationField

class Show(Model):
    title = CharField(max_length=80, unique=True)

class Episode(Model):
    show = ForeignKey(Show)
    air_date = DateField(auto_now_add=True, editable=True)
    air_time = TimeField(auto_now_add=True, editable=True)

class Song(Model):
    title = CharField(max_length=80)
    artist = CharField(max_length=80)
    length = DurationField()

class Segment(Model):
    episode = ForeignKey(Episode)
    song = ForeignKey(Song)
    time = TimeField(auto_now_add=True, editable=True)

