from django.conf.urls.defaults import *
from phytosanitary.models import Resource, Category, Photo

from phytosanitary.views import phytosanitary_resource_detail

# def get_photos(): 
#    return Photo.objects.all()

resource_info_dict = {
    'queryset': Resource.live.all(),
    'date_field': 'pub_date',
    # 'extra_context' : {"photo_list" : get_photos }
}

urlpatterns = patterns('django.views.generic.date_based',
    url(r'^$', 'archive_index', resource_info_dict, 'phytosanitary_resource_archive_index'),    
    url(r'^(?P<year>\d{4})/$', 'archive_year', resource_info_dict, 'phytosanitary_resource_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', resource_info_dict, 'phytosanitary_resource_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', resource_info_dict, 'phytosanitary_resource_archive_day'),
    # url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', resource_info_dict, 'phytosanitary_resource_detail'),
)

urlpatterns += patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', phytosanitary_resource_detail, name="phytosanitary_resource_detail"),
)