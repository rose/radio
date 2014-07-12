import sys
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from logger.models import Show, Episode, Segment, Song, Advertisement, StationID, Other


class ListShowView(ListView):
    model = Show
    template_name = "show_list.html"


class EpisodeForm(ModelForm):
    class Meta:
        model = Episode


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
        ctx['episode'] = get_object_or_404(Episode, id=self.kwargs['pk'])
        ctx['segment_list'] = Segment.objects.filter(episode=ctx['episode'])
        ctx['forms'] = [kwargs.get('Song',SongForm()),
            kwargs.get('Advertisement',AdForm()), 
            kwargs.get('StationID',IdForm()), 
            kwargs.get('Other',OtherForm())]
        ctx['seg_type'] = kwargs.get('seg_type', 'Song')
        return ctx

    def form_valid(self, form):
        form.instance.episode_id = self.kwargs['pk']
        return super(EditEpisodeView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
      self.object = None
      time = request.POST['time']
      seg_type = request.POST['seg_type'] 
      eppk = self.kwargs['pk']
      if seg_type == 'Other':
        subseg = OtherForm(**self.get_form_kwargs())
        if not subseg.is_valid():
           return self.render_to_response(
               self.get_context_data(pk=eppk,seg_type=seg_type,Other=subseg,form=SegmentForm(initial={'time':time})))
           
      created_sub = subseg.save() #TODO Check for song in db
      segargs = {
          'episode':get_object_or_404(Episode,id=eppk),
          'time': time, 
          'seg_type': ContentType.objects.get_for_model(created_sub.__class__),
          'seg_id': created_sub.pk}
      segment = Segment(**segargs)
      try:
        segment.full_clean() #TODO add try/catch to deal with validation
      except ValidationError:
        return self.render_to_response(self.get_context_data(pk=eppk,seg_type=seg_type,form=SegmentForm(instance=segment)))
      self.object = segment.save()
      return self.render_to_response(self.get_context_data(pk=eppk,seg_type=seg_type,form=SegmentForm))


