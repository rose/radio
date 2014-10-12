from random import randint
from datetime import date, timedelta
from django.db.models import * # yeah, I know.  But we're using most of them.
from django.contrib.auth.models import User
from durationfield.db.models.fields.duration import DurationField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey


# see CRTC's radio regulations 1986, as of June 2014 available at 
# http://laws.justice.gc.ca/eng/regulations/SOR-86-982/
    
class DJ(Model):
    user = OneToOneField(User)
    dj_name = CharField(max_length=80)
    #TODO separate validation for phone numbers
    phone = CharField(max_length=10, blank=True)

    def __str__(self):
        return self.dj_name


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
        return "%s with %s" % (self.title, self.dj)


class Stat(Model):
    length = DurationField(default=0)
    spoken = DurationField(default=0)
    ad_count = IntegerField(default=0)
    song_cat3 = IntegerField(default=0)
    song_cat2 = IntegerField(default=0)
    song_cat3_canadian = IntegerField(default=0)
    song_cat2_canadian = IntegerField(default=0)
    song_local = IntegerField(default=0)

    def __str__(self):
        return "Stat:  (spoken: %s of %s), (local: %s of %s), (can2: %s of %s), (can3: %s of %s), (ads: %s)" % (
            str(self.spoken),
            str(self.length),
            self.song_local,
            self.song_cat3 + self.song_cat2,
            self.song_cat2_canadian,
            self.song_cat2,
            self.song_cat3_canadian,
            self.song_cat3,
            self.ad_count
        )


class Episode(Model):
    show = ForeignKey(Show)
    stat = ForeignKey(Stat)
    air_date = DateField()
    air_time = TimeField()

    def update_stats(self, new_segment):
        content = new_segment.seg_content
        cls = content.__class__.__name__
        stat = self.stat

        # TODO these should be methods on the content classes, duhdoi
        if cls == "Song":
            if content.origin == "Lcl":
                stat.song_local += 1
            if content.category_3:
                stat.song_cat3 += 1
                if content.origin != "Int":
                    stat.song_cat3_canadian += 1
            else:
                stat.song_cat2 += 1
                if content.origin != "Int":
                    stat.song_cat2_canadian += 1

        else: # cls == "StationID" || "Other" || "Advertisement"
            if cls == "Advertisement":
                stat.ad_count += 1
            if content.spoken:
                stat.spoken += content.length

        # TODO this is very basic!
        # does not account for deletions or segments that are not played fully or many other things
        stat.length += content.length
        stat.save()
    
    def start_string(self):
        return self.air_time.strftime("%H:%M") 

    def __str__(self):
        return "%s (%s %s:%02d)" % (self.show.title, self.air_date, self.air_time.hour, self.air_time.minute)


# Segment categories, corresponding roughly to CRTC guidelines and
# (hopefully) gathering all required data

# category 5
class Advertisement(Model):
    advertiser = CharField(max_length=40)
    length = DurationField()
    spoken = BooleanField(
            choices = ((True, 'S'), (False, 'M')),
            default=True,
        )

    # required by section 8.1.c.v
    category = IntegerField(
            choices = (
                (51, "Ad"),
                (52, "Sponsor ID"),
                (53, "Promo")
            ),
            default=52
    )

    def cname(self):
      return self.__class__.__name__
    
    def __str__(self):
        return "%s, %s [%s]" % (self.get_category_display(), self.advertiser, str(self.length)[2:7])


# categories 2 and 3
# 2: pop, rock, dance; country; acoustic; easy listening
# 3: concert; folk; world/international; jazz & blues; nonclassical religious
class Song(Model):
    title = CharField(max_length=40)
    artist = CharField(max_length=40)
    composer = CharField(max_length=40)
    length = DurationField()

    category_3 = BooleanField(
            default = False,
            choices = ((True, '3'), (False, '2'))
        )
    origin = CharField(
            max_length = 3,
            choices = (
                ("Lcl", "Local"),
                ("Can", "Canadian"),
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
        return "%s (%s) [%s]" % (self.title, self.artist, str(self.length)[2:7])


# category 1 (if spoken) or 4 (if recorded musical)
class StationID(Model):
    spoken = BooleanField(
            choices = ((True, 'S'), (False, 'M')),
            default=True,
        )

    description = CharField(max_length=120)
    length = DurationField()

    def cname(self):
      return self.__class__.__name__

    def __str__(self):
        if self.spoken:
            return "Spoken ID: %s %s" % (self.description, str(self.length)[2:7])
        else:
            return "Musical ID: %s %s" % (self.description, str(self.length)[2:7])


# category 1 (spoken) or 4 (prerecorded musical, eg show themes or contest promotions)
class Other(Model):
    spoken = BooleanField(
            choices = ((True, 'S'), (False, 'M')),
            default=True,
        )


    description = CharField(max_length=120)
    length = DurationField()

    def cname(self):
      return self.__class__.__name__

    def __str__(self):
        return "%s [%s]" % (self.description, str(self.length)[:7])


class Segment(Model):
    episode = ForeignKey(Episode)
    time = TimeField()

    seg_type = ForeignKey(ContentType)
    seg_id = PositiveIntegerField()
    seg_content = GenericForeignKey('seg_type', 'seg_id')

    def get_end(self):
        dt = (datetime.datetime.combine(date.today(), self.time)
            + self.seg_content.length)
        return dt.strftime("%H:%M:%S")

    def __str__(self):
        return "Segment: %s %s [%s]" % (self.seg_content, self.episode.show.title, str(self.time)[:8])


