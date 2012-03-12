# todo

# http://www.mercurytide.co.uk/news/article/django-signals/

# import settings
# from django.conf import settings
# from django.contrib.sites.models import Site
# from django.core.mail import send_mail
# from django.db.models.signals import post_save, pre_save
# from django.template.loader import render_to_string
# 
# def send_entry_created_email(sender, instance, signal, 
#      *args, **kwargs):
#      """
#      Sends an email out to a number of people informing 
#      them of a new resource entry.
#      """
#      def get_recipient_list():
#          # Get a list of the email addresses the message
#          # should be sent to.
#          recipient_list = [item[1] for item in settings.ADMINS] # Left for you to implement.
#          return recipient_list
# 
#      try:
#          Resource.objects.get(id=instance._get_pk_val())
#      except (Resource.DoesNotExist, AssertionError):
#          # The attempt to get a resource with the same id 
#          # as our instance failed - a good indication 
#          # that this is a new resource.
#          t = loader.get_template('phytosanitary/new_resource_email.txt')
#          c = Context({
#          'resource': instance,
#          })
#          message = t.render(c)
# 
#          subject = 'A new resource was posted'
#          from_email = instance.author.email
#          recipient_list = get_recipient_list()
# 
#          email = (subject, message, from_email, recipient_list)
#          send_mass_mail(email)