from django.shortcuts import get_object_or_404, render_to_response
from coltrane.models import Category
from django.views.generic.list_detail import object_list

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return object_list(request, queryset=category.live_entry_set(), extra_context={
        'category': category
    })
# 
# def add_user(request):
#     if request.method == "POST":
#         uform = UserForm(data = request.POST)
#         pform = UserProfileForm(data = request.POST)
#         if uform.is_valid() and pform.is_valid():
#             user = uform.save()
#             profile = pform.save(commit = False)
#             profile.user = user
#             profile.save()
