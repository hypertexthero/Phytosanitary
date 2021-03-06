from django.shortcuts import get_object_or_404, render_to_response
from phytosanitary.models import Category, Resource, Contributor
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import Resource, ResourceForm, Contributor, Document, DocumentForm, Photo, PhotoForm
from django import forms

def category_detail(request, slug):
    """ categories are the site sections i.e. the global navigation """
    category = get_object_or_404(Category, slug=slug)
    return object_list(
        request, 
        queryset=category.live_resource_set(),
        paginate_by=2,
        # template_name='phytosanitary/resource_list.html', 
        extra_context={
        'category': category
        }
    )

# http://stackoverflow.com/questions/907858/how-to-let-djangos-generic-view-use-a-form-with-initial-values

# resource_upload.html
# http://stackoverflow.com/questions/569468/django-multiple-models-in-one-template-using-forms
# http://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/
@login_required
def resource_upload(request):
    if request.method == "POST":
        
        resourceform = ResourceForm(request.POST, request.FILES, instance=Resource())
        photoform = [PhotoForm(request.POST, request.FILES, prefix=str(x), instance=Photo()) for x in range(0,10)]
        documentform = [DocumentForm(request.POST, request.FILES, prefix=str(x), instance=Document()) for x in range(0,10)]
        
        user = request.user
        author_id = user.id
        
        if resourceform.is_valid() and all([pf.is_valid() for pf in photoform]) and all([df.is_valid() for df in documentform]):
            new_resource = resourceform.save(commit=False)
            new_resource.author_id = author_id
            resourceform.save()
            for pf in photoform:
                new_photo = pf.save(commit=False)
                new_photo.resource = new_resource
                pf.save()
            for df in documentform:
                new_document = df.save(commit=False)
                new_document.resource = new_resource
                df.save()
            return HttpResponseRedirect('/thanks/')
    else:
        resourceform = ResourceForm(instance=Resource())
        photoform = [PhotoForm(prefix=str(x), instance=Photo()) for x in range(0,10)]
        documentform = [DocumentForm(prefix=str(x), instance=Document()) for x in range(0,10)]
    return render_to_response('phytosanitary/resource_upload.html', {'resource_form': resourceform, 'photo_form': photoform, 'document_form': documentform},
        context_instance=RequestContext(request))


# resource_detail.html
from django.views.generic.date_based import object_detail
from django.core.urlresolvers import reverse
import datetime
import time
from django.db.models.fields import DateTimeField
from django.views.generic import date_based 
def phytosanitary_resource_detail(request, year, month, day, slug): 
    q1 = Resource.objects.all() 
    q2 = Photo.objects.all()
    q3 = Document.objects.all() 
    params = { 
        'queryset': q1, 
        'date_field': 'pub_date', 
        'year': year, 
        'month': month, 
        'day': day, 
        'slug': slug, 
        'extra_context': { 
            'photos': q2, 'documents': q3
        } 
    } 
    return date_based.object_detail(request, **params)

# search.html
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