from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
 
from coltrane.models import UserProfile
 
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["username", "email", "first_name", "last_name"] 
 
# class ProfileForm(ModelForm):
# 
#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         try:
#             self.fields['email'].initial = self.instance.user.email
#             # self.fields['first_name'].initial = self.instance.user.first_name
#             # self.fields['last_name'].initial = self.instance.user.last_name
#         except User.DoesNotExist:
#             pass
# 
#     email = forms.EmailField(label="Primary email",help_text='')
# 
#     class Meta:
#       model = Profile
#       exclude = ('user',)        
# 
#     def save(self, *args, **kwargs):
#         """
#         Update the primary email address on the related User object as well.
#         """
#         u = self.instance.user
#         u.email = self.cleaned_data['email']
#         u.save()
#         profile = super(ProfileForm, self).save(*args,**kwargs)
#         return profile