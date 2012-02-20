from django.conf.urls.defaults import patterns, include, url

# for custom registration userena form with first name and last name
from phytosanitary.coltrane.forms import SignupFormExtra

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phytosanitary.views.home', name='home'),
    # url(r'^coltrane/', include('coltrane.urls')),
    # url(r'^categories/', include('coltrane.urls.categories')), 

    url(r'^links/', include('coltrane.urls.links')), 
    url(r'^tags/', include('coltrane.urls.tags')), 
    url(r'^comments/', include('django.contrib.comments.urls')),

    # url(r'^accounts/', include('registration.backends.default.urls')), # provided by django-registration
    # url(r'^profiles/', include('profiles.urls')), # provided by django-profiles

    # http://docs.django-userena.org/en/latest/faq.html#how-do-i-add-extra-fields-to-forms
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    url(r'^accounts/', include('userena.urls')),

    url(r'^', include('coltrane.urls.entries')),

    # registration/login.html is the django default - https://docs.djangoproject.com/en/dev/topics/auth/#django.contrib.auth.views.login
    url(r'^login/$', 'django.contrib.auth.views.login'),
    # http://stackoverflow.com/questions/1296629/django-template-tag-how-to-send-next-page-in-url-auth-logout
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # moving the category slug url here from contrane/urls/categories.py
    url(r'^(?P<slug>[-\w]+)/$', 'coltrane.views.category_detail', {}, 'coltrane_category_detail'),
)


    

# urlpatterns += patterns('django.views.generic.simple',
#     # TODO: create profile pages - http://birdhouse.org/blog/2009/06/27/django-profiles/ - https://docs.djangoproject.com/en/dev/topics/auth/
#     # url(r'^profile/$', 'direct_to_template', {'template': 'profile.html'}),
#     url(r'^$', 'direct_to_template', {'template': 'base.html'}, name='home'),
# )

# TODO: categories as globalnav
# from coltrane.models import Category
# urlpatterns += patterns('',
#     (r'^$', 'django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all() }, 'coltrane_category_list'),
#     (r'^(?P<slug>[-\w]+)/$', 'coltrane.views.category_detail', {}, 'coltrane_category_detail'),
# )

# http://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-files-in-development
from django.conf import settings

if settings.DEBUG :
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )