from django.db.models import * # yeah, I know.  But we're using most of them.
from durationfield.db.models.fields.duration import DurationField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey


# see CRTC's radio regulations 1986, as of June 2014 available at 
# http://laws.justice.gc.ca/eng/regulations/SOR-86-982/
    
class DJ(Model):
    first_name = CharField(max_length=80)
    last_name = CharField(max_length=80)
    #TODO separate validation for phone numbers
    phone = CharField(max_length=10, blank=True)

    def __str__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.phone)


class Show(Model):
    title = CharField(max_length=80, unique=True)
    description = CharField(max_length=200)

    #TODO manytomany field
    dj = ForeignKey(DJ)

    # see schedule
    # local, net (with source network), rebroad, simulcast, or other
    origin_code = IntegerField(
            choices = ((1,"local"), (2,"net"), (3,"rebroad"), (4,"simulcast"), (5,"other")),
            default=1) 
    # use to generate NC code for non-canadian content, see section E
    canadian = BooleanField(default=True)
    # TODO does section C apply to CHCR or are we always X?

    def __str__(self):
        return "Show:  %s %s" % (self.title, self.dj)


class Stat(Model):
    length = DurationField()
    canadian = FloatField()
    local = FloatField()
    spoken = FloatField()


class Episode(Model):
    show = ForeignKey(Show)
    stat = ForeignKey(Stat)
    air_date = DateField()
    air_time = TimeField()

    def __str__(self):
        return "%s (%s %s)" % (self.show.title, self.air_date, self.air_time)


# Segment categories, corresponding roughly to CRTC guidelines and
# (hopefully) gathering all required data

# category 5
class Advertisement(Model):
    advertiser = CharField(max_length=40)
    length = DurationField()

    # required by section 8.1.c.v
    category = IntegerField(
            choices = (
                (51, "Announcement"),
                (52, "Sponsor ID"),
                (53, "Promotion with sponsor ID")
            ),
            default=52
    )

    def cname(self):
      return self.__class__.__name__
    
    def __str__(self):
        return "Ad:  %s, Category %d" % (self.advertiser, self.category)


# categories 2 and 3
# 2: pop, rock, dance; country; acoustic; easy listening
# 3: concert; folk; world/international; jazz & blues; nonclassical religious
class Song(Model):
    title = CharField(max_length=40)
    artist = CharField(max_length=40)
    composer = CharField(max_length=40)
    length = DurationField()

    category_3 = BooleanField(default=False)
    origin = CharField(
            max_length = 3,
            choices = (
                ("Lcl", "Local"),
                ("Can", "Non-local Canadian"),
                ("Int", "International")
            ), 
            default = "Int"
    )
    hit = BooleanField(default=False)
    # instrumental pieces must be marked!  Do it here.
    language = CharField(max_length=20, default="english")

    def cname(self):
      return self.__class__.__name__

    def __str__(self):
        return "Song: %s (%s) [%s]" % (self.title, self.artist, str(self.length)[:7])


# category 1 (if spoken) or 4 (if recorded musical)
class StationID(Model):
    spoken = BooleanField(default=True)
    length = DurationField()

    def cname(self):
      return self.__class__.__name__

    def __str__(self):
        if self.spoken:
            return "STID: Spoken"
        else:
            return "STID: Musical"


# category 1 (spoken) or 4 (prerecorded musical, eg show themes or contest promotions)
class Other(Model):
    spoken = BooleanField(default = True)
    description = CharField(max_length=120)
    length = DurationField()

    def cname(self):
      return self.__class__.__name__

    def __str__(self):
        return "Other: %s" % self.description


class Segment(Model):
    episode = ForeignKey(Episode)
    time = TimeField()

    seg_type = ForeignKey(ContentType)
    seg_id = PositiveIntegerField()
    seg_content = GenericForeignKey('seg_type', 'seg_id')

    def __str__(self):
        return "Segment: %s %s [%s]" % (self.seg_content, self.episode.show.title, str(self.time)[:8])


