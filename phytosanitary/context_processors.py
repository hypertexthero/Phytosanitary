# # http://stackoverflow.com/questions/639792/setting-object-owner-with-generic-create-object-view-in-django
# from django.views.generic.create_update import get_model_and_form_class
# 
# # from models import Resource
# 
# def form_user_default(request):
#     if request.method == 'GET':
#         model, custom_form = get_model_and_form_class(Resource,None)
#         custom_form.author = request.user
#         return {'form':custom_form}
#     else: return {}