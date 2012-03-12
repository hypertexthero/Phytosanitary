from django.contrib import admin
from phytosanitary.models import Category, Resource, Contributor, Document, Photo

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Category, CategoryAdmin)

from django.db import models
from django import forms
from django.forms import ModelForm, Textarea

class PhotoInline(admin.StackedInline):
    model = Photo

class DocumentInline(admin.StackedInline):
    model = Document

# http://stackoverflow.com/a/911915/412329
class DifferentlySizedTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        attrs.setdefault('cols', 80)
        attrs.setdefault('rows', 40)
        super(DifferentlySizedTextarea, self).__init__(*args, **kwargs)

class ResourceAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField: {'widget': DifferentlySizedTextarea}}
    exclude = ('enable_comments', 'author',)
    save_on_top = True
    list_display = ('title', 'pub_date', 'author')
    list_filter = ('status', 'pub_date', 'author')
    prepopulated_fields = { 'slug': ['title'] }
    inlines = [PhotoInline, DocumentInline]
        
    # http://www.b-list.org/weblog/2008/dec/24/admin/
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Resource, ResourceAdmin)
admin.site.register(Photo)
admin.site.register(Document)



# Alternative integration of Markedit (currently doing it with override in tempaltes/admin/base.html)
# from markedit.admin import MarkEditAdmin
# class ResourceAdmin(MarkEditAdmin):
#     exclude = ('enable_comments',)
#     save_on_top = True
#     list_display = ('title', 'pub_date', 'author')
#     prepopulated_fields = { 'slug': ['title'] }
# 
#     class MarkEdit:
#         fields = ['body', ]
#         options = {
#             'preview': 'below',
#             # 'toolbar': { 'backgroundMode' : 'light' }
#         }
#     
#     # http://www.b-list.org/weblog/2008/dec/24/admin/
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.author = request.user
#         obj.save()
# 
# admin.site.register(Resource, ResourceAdmin)