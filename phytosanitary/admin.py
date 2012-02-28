from django.contrib import admin
from phytosanitary.models import Category, Resource, MyProfile#, Link

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Category, CategoryAdmin)


class ResourceAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'pub_date', 'author')
    prepopulated_fields = { 'slug': ['title'] }
    
    # http://www.b-list.org/weblog/2008/dec/24/admin/
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Resource, ResourceAdmin)


# class MyProfileAdmin(admin.ModelAdmin):
#     pass
#     
# admin.site.register(MyProfile, MyProfileAdmin)

# class LinkAdmin(admin.ModelAdmin):
#     prepopulated_fields = { 'slug': ['title'] }
#     
# admin.site.register(Link, LinkAdmin)
