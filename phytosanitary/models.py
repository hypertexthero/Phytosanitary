import datetime
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _ 
from django.db import models
from markdown import markdown
from tagging.fields import TagField, Tag
import tagging

from django.db.models.signals import post_save # http://stackoverflow.com/a/965883/412329
from django.dispatch import receiver # https://docs.djangoproject.com/en/dev/topics/signals/#receiver-functions

from userena.models import UserenaBaseProfile

class Contributor(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='contributor')
    
    class Meta:
        ordering = ['user']
        verbose_name_plural = "Contributor user profiles"
    
    def __str__(self):
        return self.user

# add users who register using front-end form to the 'contributors' group automatically
# http://stackoverflow.com/a/8949526/412329
@receiver(post_save, sender=User, dispatch_uid='phytosanitary-project.phytosanitary.models.user_post_save_handler')
def user_post_save(sender, instance, created, **kwargs):
    """ This method is executed whenever an user object is saved - automatically adding users who register using the front-end form to the 'contributors' group                                                                                     
    """
    if created:
        instance.groups.add(Group.objects.get(name='contributor'))

class Category(models.Model):
    """ Categories are the site sections i.e. the global navigation """
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Suggested value automatically generated from title. Must be unique.")
    description = models.TextField(help_text='Use Markdown format')
    description_html = models.TextField(editable=False, blank=True)
    order = models.IntegerField()
    
    def live_resource_set(self):
        from phytosanitary.models import Resource
        return self.resource_set.filter(status=Resource.LIVE_STATUS)
        
    class Meta: 
        ordering = ['order']
        verbose_name_plural = "Categories"
    
    def __unicode__(self):
        return self.title
    
    # markdown for category description
    def save(self, force_insert=False, force_update=False):
        self.description_html = markdown(self.description)
        super(Category, self).save(force_insert, force_update)
    
    @models.permalink
    def get_absolute_url(self):
        return ('phytosanitary_category_detail', (), { 'slug': self.slug })


class LiveResourceManager(models.Manager):
    def get_query_set(self):
        return super(LiveResourceManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

# todo - better file storage:
# http://stackoverflow.com/a/1190866/412329
# def content_file_name(instance, filename):
    # return '/%Y/%m/'.join(['content', instance.user.username, filename])

class Resource(models.Model):
    LIVE_STATUS = 1
    FOR_REVIEW_STATUS = 2
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (FOR_REVIEW_STATUS, 'For Review'),
    )
    
    CONTACT_TYPE_CHOICES = (
        ('R', 'RPPO'),
        ('N', 'NPPO'),
        ('O', 'Other'),
    )

    # Core fields.
    title = models.CharField(max_length=250)
    # excerpt = models.TextField(blank=True)
    body = models.TextField(help_text='Use Markdown format', verbose_name='Description')
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name='Publication Date', help_text='(will only be published when approved by an administrator)')
    org_title = models.CharField(max_length=250, help_text='', verbose_name='Organization', blank=True)
    # http://stackoverflow.com/a/1190866/412329
    file = models.FileField(max_length=250, help_text='Files can be 10Mb maximum. You can upload files such as photos, documents and presentations.', verbose_name='Upload a file', blank=True, upload_to='%Y/%m/%d/') 
    # OLD - do not usefile = models.FileField('Upload', upload_to='files/%Y/%m%d%H%M%S/')
    url = models.URLField(blank=True, help_text="A link to something elsewhere.")
    contact_type = models.CharField(blank=True, max_length=1, choices=CONTACT_TYPE_CHOICES, default=1)
    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True, verbose_name='Address')
    agreement = models.BooleanField(verbose_name='Permission to Publish', help_text='Do you agree to have these Phytosanitary Technical Resources published in public?')

    # Fields to store generated HTML.
    # excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # Metadata.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date')
    status = models.IntegerField(choices=STATUS_CHOICES, default=FOR_REVIEW_STATUS)

    # Categorization.
    categories = models.ManyToManyField(Category)
    tags = TagField()
    
    # Need to be this way around so that non-live resources will show up in Admin, which uses the default (first) manager.
    objects = models.Manager()
    live = LiveResourceManager()
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Resources"

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        # if self.excerpt:
        #     self.excerpt_html = markdown(self.excerpt)
        super(Resource, self).save(force_insert, force_update)
    
    @models.permalink
    def get_absolute_url(self):
        return ('phytosanitary_resource_detail', (), {  'year': self.pub_date.strftime("%Y"),
                                                'month': self.pub_date.strftime("%b").lower(),
                                                'day': self.pub_date.strftime("%d"),
                                                'slug': self.slug })


# tagging users django-tagging
# See http://blog.sveri.de/index.php?/archives/139-django-tagging.html
tagging.register(Resource, tag_descriptor_attr='etags')







# FOR FUTURE USE:

# class Link(models.Model):
#     # Metadata.
#     enable_comments = models.BooleanField(default=True)
#     post_elsewhere = models.BooleanField('Post to Delicious', default=True, help_text='If checked, this will be posted both to your weblog and to your delicious.com account. (Currently disabled)')
#     posted_by = models.ForeignKey(User)
#     pub_date = models.DateTimeField(default=datetime.datetime.now)
#     slug = models.SlugField(unique_for_date='pub_date', help_text='Must be unique for the publication date.')
#     title = models.CharField(max_length=250)
#     
#     # The actual link bits.
#     description = models.TextField(blank=True)
#     description_html = models.TextField(editable=False, blank=True)
#     via_name = models.CharField('Via', max_length=250, blank=True, help_text='The name of the person whose site you spotted the link on. Optional.')
#     via_url = models.URLField('Via URL', blank=True, help_text='The URL of the site where you spotted the link. Optional.')
#     url = models.URLField('URL', unique=True)
#     tags = TagField()
#     
#     class Meta:
#         ordering = ['-pub_date']
#         
#     def __unicode__(self):
#         return self.title
#     
#     def save(self):
#         if not self.id and self.post_elsewhere:
#             import pydelicious
#             from django.utils.encoding import smart_str
#             pydelicious.add(settings.DELICIOUS_USER, 
#                             settings.DELICIOUS_PASSWORD, 
#                             smart_str(self.url), 
#                             smart_str(self.title), 
#                             smart_str(self.tags))
#         if self.description:
#             self.description_html = markdown(self.description)
#         super(Link, self).save()
#     
#     @models.permalink
#     def get_absolute_url(self):
#         return ('phytosanitary_link_detail', (), {   'year': self.pub_date.strftime('%Y'),
#                                                 'month': self.pub_date.strftime('%b').lower(),
#                                                 'day': self.pub_date.strftime('%d'),
#                                                 'slug': self.slug })

# tagging users django-tagging
# See http://blog.sveri.de/index.php?/categories/2-Django
# tagging.register(Link, tag_descriptor_attr='etags')



# The first comment moderation system...
#
# from akismet import Akismet
# from django.conf import settings
# from django.contrib.comments.models import Comment
# from django.contrib.comments.signals import comment_will_be_posted
# from django.contrib.sites.models import Site
# from django.core.mail import mail_managers
# from django.utils.encoding import smart_str
# 
# def moderate_comment(sender, comment, request, **kwargs):
#     if not comment.id:
#         resource = comment.content_object
#         delta = datetime.datetime.now() - resource.pub_date
#         if delta.days > 30:
#             comment.is_public = False
#         else:
#             akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url="http:/%s/" %Site.objects.get_current().domain)
#             if akismet_api.verify_key():
#                 akismet_data = { 'comment_type': 'comment',
#                                  'referrer': request.META['HTTP_REFERER'],
#                                  'user_ip': comment.ip_address,
#                                  'user-agent': request.META['HTTP_USER_AGENT'] }
#                 if akismet_api.comment_check(smart_str(comment.comment),
#                                             akismet_data,
#                                             build_data=True):
#                     comment.is_public = False
#         email_body = "%s posted a new comment on the resource '%s'."
#         mail_managers("New comment posted", email_body % (comment.name, comment.content_object))
#                     
# comment_will_be_posted.connect(moderate_comment, sender=Comment)


# The second comment moderation system...

# from akismet import Akismet
# from django.conf import settings
# from django.contrib.comments.moderation import CommentModerator, moderator
# from django.contrib.sites.models import Site
# from django.utils.encoding import smart_str
# 
# class ResourceModerator(CommentModerator):
#     auto_moderate_field = 'pub_date'
#     moderate_after = 30
#     email_notification = True
#     
#     def moderate (self, comment, content_object, request):
#         already_moderated = super(ResourceModerator, self).moderate(comment, content_object, request)
#         if already_moderated:
#             return True
#         akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url="http:/%s/" %Site.objects.get_current().domain)
#         if akismet_api.verify_key():
#             akismet_data = { 'comment_type': 'comment',
#                              'referrer': request.META['HTTP_REFERER'],
#                              'user_ip': comment.ip_address,
#                              'user-agent': request.META['HTTP_USER_AGENT'] }
#             return akismet_api.comment_check(smart_str(comment.comment),
#                                 akismet_data,
#                                 build_data=True)
#         return False
#         
# moderator.register(Resource, ResourceModerator)
