# from django.db import models
# from django.forms import ModelForm
# from coltrane.models import UserProfile
# from django.contrib.auth.models import User
 
from django import forms
# http://docs.django-userena.org/en/latest/faq.html
from django.utils.translation import ugettext_lazy as _
from userena.forms import SignupForm

class SignupFormExtra(SignupForm):
    """
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.


    """
    first_name = forms.CharField(label=_(u'First name'),
                                 max_length=30,
                                 required=False)

    last_name = forms.CharField(label=_(u'Last name'),
                                max_length=30,
                                required=False)

    def __init__(self, *args, **kw):
        """

        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-2]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        self.fields.keyOrder = new_order

    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ["username", "email", "first_name", "last_name"] 
 
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