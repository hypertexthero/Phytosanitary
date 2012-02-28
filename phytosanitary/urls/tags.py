from django.conf.urls.defaults import *
from phytosanitary.models import Resource
from tagging.models import Tag


urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset': Tag.objects.all(),
        'template_name': 'phytosanitary/tag_list.html'
    }, 'phytosanitary_tag_list'),
    
    (r'^(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', { 
        'queryset_or_model': Resource.live.all(), 
        'template_name': 'phytosanitary/resources_by_tag.html'
    }, 'phytosanitary_resource_archive_tag'),
    
    # (r'^links/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', {
    #     'queryset_or_model': Link.objects.all(),
    #     'template_name': 'phytosanitary/links_by_tag.html'
    # }, 'phytosanitary_link_archive_tag'),
)