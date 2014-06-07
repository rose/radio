from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
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


class EditEpisodeView(ListView):
    template_name = "edit_episode.html"

    def get_queryset(self):
        self.ep = get_object_or_404(Episode, id=self.kwargs['pk'])
        return Segment.objects.filter(episode=self.ep)

    def get_context_data(self, **kwargs):
        ctx = super(EditEpisodeView, self).get_context_data(**kwargs)
        ctx['episode'] = self.ep
        return ctx
