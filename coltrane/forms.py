from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
 
from coltrane.models import UserProfile
 
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["username", "email"]
 
 

# class UserProfileForm(ModelForm):
#   def __init__(self, *args, **kwargs):
#       super(UserProfileForm, self).__init__(*args, **kwargs)
#       try:
#           self.fields['email'].initial = self.instance.user.email
#       except User.DoesNotExist:
#           pass
# 
#   email = forms.EmailField(label="Primary email")
# 
#   class Meta:
#     model = User
#     fields = ["first_name", "last_name", "email"]
# 
#   def save(self, *args, **kwargs):
#     """
#     Update the primary email address on the related User object as well. 
#     """
#     u = self.instance.user
#     u.email = self.cleaned_data['email']
#     u.save()
#     profile = super(UserProfileForm, self).save(*args,**kwargs)
#     return profile
    

# class ProfileForm(ModelForm):
#   class Meta:
#       model = UserProfile
      # fields = ["username", "email", "first_name", "last_name"]
      # app_label = 'profiles'
      # exclude = ('username',)
