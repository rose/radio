from django.forms import ModelForm, Form, TextInput, RadioSelect
from logger.models import *
from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteSelectField


class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = ['air_date', 'air_time']
        widgets = {
            'air_date': TextInput(attrs={
                'size': '16', 'placeholder': 'Air Date MM/DD/YY',
                'title': 'Air Date MM/DD/YY'}),
            'air_time': TextInput(attrs={
                'size': '16', 'placeholder': 'Air Time (HH:MM)',
                'title': 'Air Time (HH:MM 24hr format)'})
        }
        labels = {'air_date': '', 'air_time': ''}

class SegmentForm(ModelForm):
    class Meta:
        model = Segment
        fields = ['time',]
        widgets = {
            'time': TextInput(attrs={
                'size':'8', 'placeholder': 'Start', 
                'title': 'Start Time (HH:MM 24hr format)'}),
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
            'title': TextInput(attrs={
                'size': '16', 'placeholder' : 'Title', 'title' : 'Title'}), 
            'artist': TextInput(attrs={
                'size': '16', 'placeholder': 'Artist', 'title' : 'Artist'}),
            'composer': TextInput(attrs={
                'size': '16', 'placeholder': 'Composer', 
                'title' : 'Composer'}),
            'length': TextInput(attrs={
                'size': '8', 'placeholder': 'Length', 'title' : 'Length (MM:SS)'}),
        }
        labels = {
            'title': '', 'artist': '', 'composer': '', 'length': '',
        }

class AdvertisementForm(ModelForm):
    class Meta:
        model = Advertisement
        widgets = {
            'advertiser' : TextInput(attrs={
                'size': '16', 'placeholder': 'Advertiser',
                'title': 'Advertiser'}),
            'length': TextInput(attrs={
                'size': '8', 'placeholder': 'Length', 
                'title' : 'Length (MM:SS)'}),
            'category': RadioSelect(),
        }
        labels = {
            'advertiser': '', 'length': '',
        }

class StationIDForm(ModelForm):
    class Meta:
        model = StationID
        widgets = {
            'length': TextInput(attrs={
                'size': '8', 'placeholder': 'Length', 'title' : 'Length (MM:SS)'}),
        }
        labels = {
            'length': '',
        }


class OtherForm(ModelForm):
    class Meta:
        model = Other
        widgets = {
            'description' : TextInput(attrs={
                'size': '16', 'placeholder': 'Description',
                'title': 'Description'}),
            'length': TextInput(attrs={
                'size': '8', 'placeholder': 'Length', 'title' : 'Length (MM:SS)'}),
        }
        labels = {
            'description': '', 'length': '',
        }



