from django.contrib import admin
from phytosanitary.models import Category, Resource, Contributor#, Link

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Category, CategoryAdmin)


class ResourceAdmin(admin.ModelAdmin):
    exclude = ('enable_comments',)
    save_on_top = True
    list_display = ('title', 'pub_date', 'author')
    prepopulated_fields = { 'slug': ['title'] }
    
    # http://www.b-list.org/weblog/2008/dec/24/admin/
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Resource, ResourceAdmin)



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