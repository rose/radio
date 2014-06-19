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


class EpisodeSegmentsView(ListView):
    template_name = "edit_episode.html"

    def get_queryset(self):
        self.ep = get_object_or_404(Episode, id=self.kwargs['pk'])
        return Segment.objects.filter(episode=self.ep)

    def get_context_data(self, **kwargs):
        ctx = super(EpisodeSegmentsView, self).get_context_data(**kwargs)
        ctx['episode'] = self.ep
        ctx['form'] = SegmentForm()
        return ctx


class SegmentForm(ModelForm):
    class Meta:
        model = Segment
        fields = ['song', 'time']


class AddSegmentView(CreateView):
    model = Segment
    form_class = SegmentForm
    template_name = 'edit_episode.html'

    def form_valid(self, form):
        form.instance.episode_id = self.kwargs['pk']
        return super(AddSegmentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('edit-episode', kwargs={'pk': self.object.episode.pk})


class EditEpisodeView(View):
    def get(self, request, *args, **kwargs):
        view = EpisodeSegmentsView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AddSegmentView.as_view()
        return view(request, *args, **kwargs)
