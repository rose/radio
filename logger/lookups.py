from django.utils.html import escape
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from ajax_select import LookupChannel
from logger.models import Song, Advertisement, Other

class SongLookup(LookupChannel):
    model = Song

    def get_query(self,q,request):
        return Song.objects.filter(Q(title__icontains=q) | Q(artist__icontains=q) | Q(composer__icontains=q)).order_by('title')
        

    def get_result(self,obj):
        return obj.title 

    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s" % (escape(str(obj)))

