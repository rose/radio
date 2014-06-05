from django.shortcuts import render
from django.views.generic import ListView
from logger.models import Show, Episode, Segment, Song

class ListShowView(ListView):
    model = Show
    template_name = "show_list.html"

class EditShowView(ListView):
    model = Episode
    template_name = "edit_show.html"
