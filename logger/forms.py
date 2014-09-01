from django.forms import ModelForm, Form, TextInput
from logger.models import *
from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteSelectField


class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = ['air_date', 'air_time']

class SegmentForm(ModelForm):
    class Meta:
        model = Segment
        fields = ['time',]
        widgets = {
            'time': TextInput(
              attrs={'size':'8', 'placeholder': 'Start'}),
        }
        labels = {
            'time': '',
        }

        
class AutoSongForm(Form):
    Song = AutoCompleteSelectField('songs', help_text=None)

class AutoAdvertisementForm(Form):
    Advertisement = AutoCompleteSelectField('ads', help_text=None)

class AutoStationIDForm(Form):
    StationID = AutoCompleteSelectField('ids', help_text=None)

class AutoOtherForm(Form):
    Other = AutoCompleteSelectField('others', help_text=None)
    
class SongForm(ModelForm):
    class Meta:
        model = Song
        widgets = {
            'title': TextInput(
              attrs={'size': '16', 'placeholder' : 'Title'}),    
            'artist': TextInput(
              attrs={'size': '16', 'placeholder': 'Artist'}),
            'composer': TextInput(
              attrs={'size': '16', 'placeholder': 'Composer'}),
            'length': TextInput(
              attrs={'size': '8', 'placeholder': 'Length'}),
        }
        labels = {
            'title': '', 'artist': '', 'composer': '', 'length': '',
        }

class AdvertisementForm(ModelForm):
    class Meta:
        model = Advertisement

class StationIDForm(ModelForm):
    class Meta:
        model = StationID

class OtherForm(ModelForm):
    class Meta:
        model = Other


