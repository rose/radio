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
