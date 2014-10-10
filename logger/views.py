import sys
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import redirect_to_login
from django.views.generic import ListView, CreateView, View
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponseNotFound
from logger.forms import *
from logger.models import *


class ListShowView(ListView):
    model = Show
    template_name = "show_list.html"

class EditShowView(CreateView):
    template_name = "edit_show.html"
    form_class = EpisodeForm

    def post(self, request, *args, **kwargs):
        show_pk = self.kwargs['pk']
        self.show = get_object_or_404(Show, id=show_pk)
        if not all((request.user.is_authenticated(), 
            request.user.id == self.show.dj.user.id)):
                return redirect_to_login(request.path, reverse('login'))
        else:
            return super(EditShowView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(EditShowView, self).get_context_data(**kwargs)
        ctx['show'] = get_object_or_404(Show, id=self.kwargs['pk'])
        ctx['episode_list'] = Episode.objects.filter(show=ctx['show'])
        return ctx

    def form_valid(self, form):
        form.instance.show_id = self.kwargs['pk']
        stat = Stat()
        stat.save()
        form.instance.stat_id = stat.id
        return super(EditShowView, self).form_valid(form)

    def get_success_url(self):
        return reverse('edit-show', kwargs={'pk': self.object.show.pk})


class EditEpisodeView(CreateView):
    template_name = "edit_episode.html"
    form_class = SegmentForm

    def get_context_data(self, **kwargs):
        ctx = super(EditEpisodeView, self).get_context_data(**kwargs)
        ctx['episode'] = get_object_or_404(Episode, id = self.kwargs['pk'])
        #TODO sorting by time will be wrong for shows that cross midnight
        ctx['segment_list'] = Segment.objects.filter(episode = ctx['episode']).order_by('-time')
        if ctx['segment_list']:
            ctx['last_seg_time'] = ctx['segment_list'][0].get_end()
        else:
        #If there aren't any segments, use the start time of the episode
            ctx['last_seg_time'] = ctx['episode'].start_string()
        ctx['forms'] = { 
            'AutoSong': AutoSongForm(),
            'AutoAdvertisement': AutoAdvertisementForm(), 
            'AutoStationID': AutoStationIDForm(), 
            'AutoOther': AutoOtherForm(), 
            'Song': SongForm(), 
            'Advertisement': AdvertisementForm(), 
            'StationID': StationIDForm(), 
            'Other': OtherForm(), 
        }
        ctx['seg_type'] = kwargs.get('seg_type', 'Song')
        ctx['seg_auto'] = kwargs.get('seg_auto', True)
        ctx['ordered_names'] = ['Song', 'Advertisement', 'StationID', 'Other']
        return ctx

    def form_valid(self, form):
        form.instance.episode_id = self.kwargs['pk']
        return super(EditEpisodeView, self).form_valid(form)


    def get_content_form(self,request):
        self.auto = False
        if self.seg_type not in ['Song', 'Advertisement', 'StationID', 'Other']:
            return HttpResponseNotFound(
                "<h1>Can't add a " + self.seg_type + 
                ' to the database because there is no such thing.</h1>'
                )
        seg_text = self.seg_type + '_text'
        if request.POST[seg_text] == '' and request.POST[self.seg_type] == '': #Creating a new sub-segment
            self.form_type = self.seg_type
            ContentForm = globals()[self.seg_type + 'Form']
            content_form = ContentForm(**self.get_form_kwargs())
        else: #Using an existing segment
            self.form_type = 'Auto' + self.seg_type 
            self.auto = True
            ContentForm = globals()[self.form_type + 'Form']
            content_form = ContentForm(request.POST)
        return content_form


    def post(self, request, *args, **kwargs):
        self.object = None
        self.seg_type = request.POST['seg_type']
        time = request.POST['time']
        episode_pk = self.kwargs['pk']
        self.episode = get_object_or_404(Episode, id=episode_pk)
        if not all((request.user.is_authenticated(), 
            request.user.id == self.episode.show.dj.user.id)):
                return redirect_to_login(request.path, reverse('login'))

        ctx = self.get_context_data(pk=episode_pk, seg_type=self.seg_type)

        seg_form = SegmentForm( {'time': time} )
        content_form = self.get_content_form(request)

        if not content_form.is_valid() or not seg_form.is_valid():
            ctx['form'] = seg_form
            ctx['forms'][self.form_type] = content_form
            ctx['seg_auto'] = self.auto
            return self.render_to_response(ctx)

        if self.auto:
            created_sub = content_form.cleaned_data.get(self.seg_type) 
        else:
            created_sub = content_form.save() 

        segargs = {
            'episode': self.episode,
            'time': time, 
            'seg_type': ContentType.objects.get_for_model(created_sub.__class__),
            'seg_id': created_sub.pk
        }
        segment = Segment(**segargs)

        segment.episode.update_stats(segment)

        self.object = segment.save()
        ctx = self.get_context_data(pk=episode_pk, seg_type=self.seg_type,
                seg_auto=self.auto)
        ctx['form'] = SegmentForm()
        return self.render_to_response(ctx)

def logout_view(request):
    logout(request)
    return redirect_to_login(request.META['HTTP_REFERER'], reverse('login'))
