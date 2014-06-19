from django.db.models import Model, CharField, DateField, TimeField, ForeignKey
from durationfield.db.models.fields.duration import DurationField


class Show(Model):
    title = CharField(max_length=80, unique=True)

    def __str__(self):
        return self.title


class Episode(Model):
    show = ForeignKey(Show)
    air_date = DateField(auto_now_add=True, editable=True)
    air_time = TimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return "%s (%s %s)" % (self.show.title, self.air_date, self.air_time)


class Song(Model):
    title = CharField(max_length=80)
    artist = CharField(max_length=80)
    length = DurationField()

    def __str__(self):
        return "%s %s %s" % (self.title, self.artist, self.length)


class Segment(Model):
    episode = ForeignKey(Episode)
    song = ForeignKey(Song)
    time = TimeField(editable=True)

    def __str__(self):
        return "%s %s %s" % (self.song.title, self.episode.show.title, self.time)

