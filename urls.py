from django.conf.urls.defaults import patterns, include, url
from phytosanitary.forms import SignupFormExtra # for custom registration userena form with first name and last name
from django.views.generic.simple import direct_to_template

from django.contrib import admin 
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tags/', include('phytosanitary.urls.tags')), 
    url(r'^comments/', include('django.contrib.comments.urls')),
    # http://docs.django-userena.org/en/latest/faq.html#how-do-i-add-extra-fields-to-forms
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    url(r'^accounts/', include('userena.urls')),

    # registration/login.html is the django default - https://docs.djangoproject.com/en/dev/topics/auth/#django.contrib.auth.views.login
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    # http://stackoverflow.com/questions/1296629/django-template-tag-how-to-send-next-page-in-url-auth-logout
    # url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    
    # home
    url(r'^', include('phytosanitary.urls.resources')),    
    # search
    url(r'^search/', 'phytosanitary.views.search', name="resources_search"),

    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # contributor upload form
    url(r'^upload/$', 'phytosanitary.views.resource_upload', name='resource_upload'),
    # url(r'^upload/$', 'django.views.generic.create_update.create_object', kwargs={'context_processors':form_user_default}),
    url(r'^thanks/$', direct_to_template, {'template': 'phytosanitary/resource_upload_thanks.html'}),

    # section/cateogry/globalnav - moving the category slug url here from contrane/urls/categories.py
    url(r'^(?P<slug>[-\w]+)/$', 'phytosanitary.views.category_detail', {}, 'phytosanitary_category_detail'),
)

# http://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-files-in-development
from django.conf import settings
if settings.DEBUG :
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )