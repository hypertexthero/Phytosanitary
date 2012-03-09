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


# http://stackoverflow.com/questions/907858/how-to-let-djangos-generic-view-use-a-form-with-initial-values
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import Resource, ResourceForm, Contributor, Photo
from django import forms

def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

import tempfile
import shutil

# FILE_UPLOAD_DIR = '/home/imran/uploads'
# def handle_uploaded_file(source):
#     fd, filepath = tempfile.mkstemp(prefix=source.name, dir=MEDIA_ROOT)
#     with open(filepath, 'wb') as dest:
#         shutil.copyfileobj(source, dest)
#     return filepath

@login_required
def resource_upload(request):
    if request.method == 'POST':
        # Get data from form
        # including any files - https://docs.djangoproject.com/en/1.3/topics/http/file-uploads/
        form = ResourceForm(request.POST, request.FILES, initial={'author': request.user})
        
        # title = object.title
        user = request.user
        author_id = user.id
        # slug = "%s" % (self.title)
        # document = request.FILES['document']
        
        # If the form is valid, create a new object and redirect to thanks page.
        if form.is_valid(): 
            # http://www.mail-archive.com/django-users@googlegroups.com/msg80485.html
            # > However a much better way is not to have the user_id field in the form
            # >> at all, and set the correct value on the object on save.
            newObject = form.save(commit=False)
            newObject.author_id = author_id
            newObject.save()
            form.save_m2m() # needed since using commit=False
            # return HttpResponseRedirect(newObject.get_absolute_url())

            return HttpResponseRedirect('/thanks/')

    else:
        # Fill in the field with the current user by default
        # Eureka!! http://stackoverflow.com/questions/907858/how-to-let-djangos-generic-view-use-a-form-with-initial-values
        form = ResourceForm(initial={'author': request.user})
    
    # Render our template
    return render_to_response('phytosanitary/resource_upload.html',
        {'form': form},
        context_instance=RequestContext(request))











from django.views.generic.date_based import object_detail
from django.core.urlresolvers import reverse
import datetime
import time
from django.db.models.fields import DateTimeField
# def get_photos(): 
#    return Photo.objects.all()


from django.views.generic import date_based 
# from yourproj.yourapp.models import Thing1 
# from yourproj.yourotherapp.models import Thing2 
def phytosanitary_resource_detail(request, year, month, day, slug): 
    q1 = Resource.objects.all() 
    q2 = Photo.objects.all() 
    params = { 
        'queryset': q1, 
        'date_field': 'pub_date', 
        'year': year, 
        'month': month, 
        'day': day, 
        'slug': slug, 
        'extra_context': { 
            'photos': q2 
        } 
    } 
    return date_based.object_detail(request, **params)

# def phytosanitary_resource_detail(request, year, month, day, slug):
#     """View resource detail"""
# 
#     # photos=Photo.objects.all()
# 
#     return object_detail(request,
#         queryset=Resource.objects.all(),
#         # photos=Photo.objects.all(),
#         year='year',
#         month='month',
#         day='day',
#         slug='slug',
#         slug_field='slug',
#         date_field='pub_date',
#         template_name='phytosanitary/resource_detail.html',
#         template_object_name='object', # so I can write {{ note.title }} in templates/notes/detail.html (otherwise I would need to write {{ object.title }})   
#         # extra_context= { 'photos': photos },
#     )






# from django.views.generic.create_update import create_object
# # from django.contrib.auth.decorators import login_required # for @login_required decorator
# from django.core.urlresolvers import reverse
# from models import Resource, ResourceForm, Contributor
# from django.contrib.auth.models import User
# # from context_processors import form_user_default
# 
# # see also this alternative: http://djangosnippets.org/snippets/966/
# # http://www.b-list.org/weblog/2008/nov/09/dynamic-forms/
# 
# # @login_required
# def resource_upload(request):
#     """ Form for contributors to upload resources. These should have 'For Review' status. """
#     # user = Resource.objects.filter(owner__username__exact=username)
#     # user = request.user
#     # author = Resource.objects.get(pk=user)
#     author = request.user
#     # author_id = author
#     return create_object(request,
#         # model=Resource,
#         form_class=ResourceForm,
#         # form_class=ResourceForm, # Needed to specify form_class instead of model so that the custom date widget for dropdown menu is displayed: https://docs.djangoproject.com/en/dev/ref/generic-views/#django-views-generic-create-update-create-object
#         extra_context={'User': 'user', 'author': request.user, 'author_id': request.user.id }, # needed to capitalize 'User' for this to work so it would call the function!
#         login_required=True,
#         template_name='phytosanitary/resource_upload.html',
#         # post_save_redirect=reverse("notes_list")
#         # post_save_redirect="/notes/archive/%(id)s/" # todo: add object.get_absolute_url() to models.py
#         post_save_redirect="/thanks/"
#         # context_processors= ************************ try this: put context processor here ******************************* - 
#         # context_processors=[form_user_default]
#     )     
 

# 8888888888888888888888888
#     try this - put the user variable in a queryset in urls.py, then use the user variable in the view
# 8888888888888888888888888
# http://www.b-list.org/weblog/2006/nov/16/django-tips-get-most-out-generic-views/
# https://docs.djangoproject.com/en/1.3/topics/generic-views/#complex-filtering-with-wrapper-functions


# from django.views.generic.list_detail import object_list
# from myproject.myapp.models import TodoList, TodoItem
# 
# def user_lists(request, username):
#     todo_lists = TodoList.objects.filter(owner__username__exact=username)
#     open_items = TodoItem.objects.filter(todolist__owner__username__exact=username)
#     open_item_count = open_items.count()
#     priority_items = open_items.filter(priority__exact='high')
#     return object_list(request, queryset=todo_lists,
#                        extra_context={'open_item_count': open_item_count,
#                                       'priority_items': priority_items})
# And now the open_items and priority_items variables will be available, with the correct values, in the template.




















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
# from django.views.generic.list_detail import object_detail
# from django.views.generic.date_based import archive_index

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