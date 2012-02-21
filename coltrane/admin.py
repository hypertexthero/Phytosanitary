from django.contrib import admin
from phytosanitary.models import Category, Resource, Link

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Category, CategoryAdmin)


class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Resource, ResourceAdmin)


class LinkAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }
    
admin.site.register(Link, LinkAdmin)
