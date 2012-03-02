from django.shortcuts import get_object_or_404, render_to_response
from phytosanitary.models import Category, Resource, Contributor
from django.views.generic.list_detail import object_list

def category_detail(request, slug):
    """ categories are the site sections i.e. the global navigation """
    category = get_object_or_404(Category, slug=slug)
    return object_list(
        request, 
        queryset=category.live_resource_set(),  
        # template_name='phytosanitary/resource_list.html', 
        extra_context={
        'category': category
        }
    )


from django.views.generic.create_update import create_object
from django.contrib.auth.decorators import login_required # for @login_required decorator
from django.core.urlresolvers import reverse
from models import Resource
from models import ResourceForm

# see also this alternative: http://djangosnippets.org/snippets/966/
@login_required
def resource_upload(request):
    """ Form for contributors to upload resources. These should have 'For Review' status. """
    # user = Resource.objects.filter(owner__username__exact=username)
    # user = request.user
    # author = Resource.objects.get(pk=user)
    author = request.user
    # author_id = author
    return create_object(request,
        # model=Resource,
        form_class=ResourceForm,
        # form_class=ResourceForm, # Needed to specify form_class instead of model so that the custom date widget for dropdown menu is displayed: https://docs.djangoproject.com/en/dev/ref/generic-views/#django-views-generic-create-update-create-object
        extra_context={'User': 'user', 'Author': 'author'}, # needed to capitalize 'User' for this to work so it would call the function!
        template_name='phytosanitary/resource_upload.html',
        # post_save_redirect=reverse("notes_list")
        # post_save_redirect="/notes/archive/%(id)s/" # todo: add object.get_absolute_url() to models.py
        post_save_redirect="/thanks/"
    )     
 


# =todo - only display fields that have values entered in resource_detail.html:
# http://stackoverflow.com/questions/2170228/django-iterate-over-model-instance-field-names-and-values-in-template/2226150#2226150
# from django.core import serializers
# data = serializers.serialize( "python", Resource.objects.all() )



# =Search

# from django.http import HttpResponse 
# from django.template import loader, Context
# 
# def search(request): 
#     query = request.GET['q']
#     results = Note.objects.filter(body_html__icontains=query)
#     template = loader.get_template('notes/search.html')
#     context = Context({ 'query': query, 'results': results })
#     response = template.render(context)
#     return HttpResponse(response)

# or use django's render_to_response shortcut:

# def search(request):
#     query = request.GET['q']
#     return render_to_response('notes/search.html',
#         {   'query': query, 
#             'results': Note.objects.filter(body_html__icontains=query) })

# rewritten so /search/ URL can be accessed directly:

from django.shortcuts import render_to_response
from django.db.models import Q

from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_detail
from django.views.generic.date_based import archive_index

def search(request):
    """ Search form for body_html and titles so far """
    query = request.GET.get('q', '') # both /search/ and /search/?q=query work
    results = []
    user = request.user # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context
    if query:
        # INSTEAD OF THIS:
        # title_results = Note.objects.filter(title__icontains=query)
        # results = Note.objects.filter(body_html__icontains=query)
        # DO THE FOLLOWING, to avoid duplicate results when query word is both in title and body_html:
        # http://stackoverflow.com/questions/744424/django-models-how-to-filter-out-duplicate-values-by-pk-after-the-fact
        results = Resource.objects.filter(Q(title__icontains=query)|Q(body_html__icontains=query)).distinct()
    return render_to_response('phytosanitary/search.html',
        {   'query': query, 
            'results': results,
            'user': user
             })

# =todo: upload resources form for contributors
# - http://parand.com/say/index.php/2010/02/19/django-using-the-permission-system/:
def upload():
    """
        upload resources form
    
        Resource publication [moderation](https://github.com/dominno/django-moderation#readme) - permissions Groups for contributors, moderators, secretariat staff
            - Non-secretariat users who register can only submit resources for approval by a moderator or chief administrator, not publish directly to the site.
                - <del>[Users who register through front-end of site need to be automatically assigned to 'contributors' group](http://stackoverflow.com/questions/8949303/how-to-assign-a-user-to-a-group-at-signup-using-django-userena)</del> Done.
                - *Contributors can add/save a resource as Draft/for review only*
            - [Email](http://stackoverflow.com/questions/2349483/django-models-signals-and-email-sending-delay) [notification](https://github.com/jtauber/django-notification/) to moderators/staff when new resources are submitted
    
    
    """
    pass