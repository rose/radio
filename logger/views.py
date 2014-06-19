from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from logger.models import Show, Episode, Segment, Song


class ListShowView(ListView):
    model = Show
    template_name = "show_list.html"


class EditShowView(ListView):
    template_name = "edit_show.html"

    def get_queryset(self):
        self.show = get_object_or_404(Show, id=self.kwargs['pk'])
        return Episode.objects.filter(show=self.show)

    def get_context_data(self, **kwargs):
        ctx = super(EditShowView, self).get_context_data(**kwargs)
        ctx['show'] = self.show
        return ctx


class SegmentForm(ModelForm):
    class Meta:
        model = Segment
        fields = ['song', 'time']


class EditEpisodeView(CreateView):
    template_name = "edit_episode.html"
    form_class = SegmentForm

    def get_context_data(self, **kwargs):
        ctx = super(EditEpisodeView, self).get_context_data(**kwargs)
        ctx['episode'] = get_object_or_404(Episode, id=self.kwargs['pk'])
        ctx['segment_list'] = Segment.objects.filter(episode=ctx['episode'])
        return ctx

    def form_valid(self, form):
        form.instance.episode_id = self.kwargs['pk']
        return super(EditEpisodeView, self).form_valid(form)

    def get_success_url(self):
        return reverse('edit-episode', kwargs={'pk': self.object.episode.pk})




