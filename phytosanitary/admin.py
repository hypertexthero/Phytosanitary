from django.contrib import admin
from phytosanitary.models import Category, Resource, MyProfile#, Link

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Category, CategoryAdmin)


class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Resource, ResourceAdmin)


# class MyProfileAdmin(admin.ModelAdmin):
#     pass
#     
# admin.site.register(MyProfile, MyProfileAdmin)

# class LinkAdmin(admin.ModelAdmin):
#     prepopulated_fields = { 'slug': ['title'] }
#     
# admin.site.register(Link, LinkAdmin)
