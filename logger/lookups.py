from django.utils.html import escape
from ajax_select import LookupChannel
from logger.models import Song

class SongLookup(LookupChannel):
    model = Song

    def get_query(self,q,request):
        return Song.objects.filter(title__icontains=q).order_by('title')

    def get_result(self,obj):
        return obj.id

    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s <i>%s</i>" % (escape(obj.title),escape(obj.artist))

