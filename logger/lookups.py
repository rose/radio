from django.utils.html import escape
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from ajax_select import LookupChannel
from logger.models import Song, Advertisement, StationID, Other

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


class AdLookup(LookupChannel):
    model = Advertisement

    def get_query(self,q,request):
        return Advertisement.objects.filter(Q(advertiser__icontains=q)).order_by('advertiser')
        

    def get_result(self,obj):
        return obj.advertiser

    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s" % (escape(str(obj)))


class IdLookup(LookupChannel):
    model = StationID

    def get_query(self,q,request):
        return StationID.objects.filter(Q(length__gt=int(q))).order_by('length')
        

    def get_result(self,obj):
        return str(obj)

    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s" % (escape(str(obj)))


class OtherLookup(LookupChannel):
    model = Other

    def get_query(self,q,request):
        return Other.objects.filter(Q(description__icontains=q)).order_by('description')
        

    def get_result(self,obj):
        return obj.description

    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s" % (escape(str(obj)))

