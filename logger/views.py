import sys
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.forms import ModelForm, Form
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteSelectField
from logger.models import Show, Episode, Segment, Song, Advertisement, StationID, Other


class ListShowView(ListView):
    model = Show
    template_name = "show_list.html"


class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = ['air_date', 'air_time']


class EditShowView(CreateView):
    template_name = "edit_show.html"
    form_class = EpisodeForm

    def get_context_data(self, **kwargs):
        ctx = super(EditShowView, self).get_context_data(**kwargs)
        ctx['show'] = get_object_or_404(Show, id=self.kwargs['pk'])
        ctx['episode_list'] = Episode.objects.filter(show=ctx['show'])
        return ctx

    def form_valid(self, form):
        form.instance.show_id = self.kwargs['pk']
        return super(EditShowView, self).form_valid(form)

    def get_success_url(self):
        return reverse('edit-show', kwargs={'pk': self.object.show.pk})


class SegmentForm(ModelForm):
    class Meta:
        model = Segment
        fields = ['time',]
        
class AutoForm(Form):
    autocomp = AutoCompleteSelectField('songs', help_text=None)

class SongForm(ModelForm):
    class Meta:
        model = Song

class AdForm(ModelForm):
    class Meta:
        model = Advertisement

class IdForm(ModelForm):
    class Meta:
        model = StationID

class OtherForm(ModelForm):
    class Meta:
        model = Other


class EditEpisodeView(CreateView):
    template_name = "edit_episode.html"
    form_class = SegmentForm

    def get_context_data(self, **kwargs):
        ctx = super(EditEpisodeView, self).get_context_data(**kwargs)
        ctx['episode'] = get_object_or_404(Episode, id = self.kwargs['pk'])
        #TODO sorting by time will be wrong for shows that cross midnight
        ctx['segment_list'] = Segment.objects.filter(episode = ctx['episode']).order_by('time')
        ctx['forms'] = { 
            'Auto': AutoForm(),
            'Song': SongForm(), 
            'Advertisement': AdForm(), 
            'StationID': IdForm(), 
            'Other': OtherForm() 
        }
        ctx['seg_type'] = kwargs.get('seg_type', 'Song')
        ctx['ordered_names'] = ['Auto', 'Song', 'Advertisement', 'StationID', 'Other']
        return ctx

    def form_valid(self, form):
        form.instance.episode_id = self.kwargs['pk']
        return super(EditEpisodeView, self).form_valid(form)


    def post(self, request, *args, **kwargs):
        self.object = None
        seg_type = request.POST['seg_type']
        time = request.POST['time']
        episode_pk = self.kwargs['pk']

        ctx = self.get_context_data(pk=episode_pk, seg_type=seg_type)

        seg_form = SegmentForm( {'time': time} )
        if seg_type == 'Auto':
            content_form = OtherForm(**self.get_form_kwargs())
        elif seg_type == 'Song':
            content_form = SongForm(**self.get_form_kwargs())
        elif seg_type == 'Advertisement':
            content_form = AdForm(**self.get_form_kwargs())
        elif seg_type == 'StationID':
            content_form = IdForm(**self.get_form_kwargs())
        elif seg_type == 'Other':
            content_form = OtherForm(**self.get_form_kwargs())

        if not content_form.is_valid() or not seg_form.is_valid():
            ctx['form'] = seg_form
            ctx['forms'][seg_type] = content_form
            return self.render_to_response(ctx)

        if seg_type == 'Auto':
            created_sub = 
        created_sub = content_form.save() #TODO Check for song in db

        segargs = {
            'episode': get_object_or_404(Episode, id=episode_pk),
            'time': time, 
            'seg_type': ContentType.objects.get_for_model(created_sub.__class__),
            'seg_id': created_sub.pk
        }
        segment = Segment(**segargs)

        self.object = segment.save()
        ctx['form'] = SegmentForm()
        return self.render_to_response(ctx)


