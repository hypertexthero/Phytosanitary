# from django.db import models
# from django.forms import ModelForm
# from phytosanitary.models import UserProfile
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
                                 required=True)

    last_name = forms.CharField(label=_(u'Last name'),
                                max_length=30,
                                required=True)

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


# from django.forms import ModelForm
# import datetime
# from models import Resource
# from widgets import SplitSelectDateTimeWidget
# # from phytosanitary-project import settings
# import settings
# 
# # Using ModelForm here to override the model's default text input widget and have a drop down menu with selectable date and time. Also needed to specify form_class=NoteForm in the create_object and update_object generic views functions in views.py
# 
# class ResourceForm(ModelForm): 
#     pub_date = forms.DateTimeField(
#         widget = SplitSelectDateTimeWidget(
#             years=range(1978, datetime.datetime.now().year+10) # The years argument was necessary to specify a range of selectable years so an article can be set to be published automatically in a future date - http://stackoverflow.com/questions/3232364/display-a-series-of-dropdown-lists-with-past-dates-in-django
#             ), 
#         # finally fixed bug where current time to the second was not being called with the help of http://stackoverflow.com/a/2771701/412329
#         # datetime.now() was being evaluated when the model was defined, and not each time I added a record.
#         # changed:
#         # initial = datetime.datetime.now()
#         # to:
#         initial = datetime.datetime.now
#     )
#     # modified = forms.DateTimeField(widget=SplitSelectDateTimeWidget(twelve_hr=False)) 
#     class Meta:
#         model = Resource