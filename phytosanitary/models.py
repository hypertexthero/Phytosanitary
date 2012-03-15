import datetime
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _ 
from django.db import models
from markdown import markdown
from tagging.fields import TagField, Tag
import tagging
from django.template.defaultfilters import slugify

import os.path

from django.db.models.signals import post_save # http://stackoverflow.com/a/965883/412329
from django.dispatch import receiver # https://docs.djangoproject.com/en/dev/topics/signals/#receiver-functions

from userena.models import UserenaBaseProfile

class Contributor(UserenaBaseProfile):
    """ Contributor user profiles """
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
# =todo: try this alternative: http://sontek.net/extending-the-django-user-model
@receiver(post_save, sender=User, dispatch_uid='project.phytosanitary.models.user_post_save_handler')
def user_post_save(sender, instance, created, **kwargs):
    """ This method is executed whenever an user object is saved - automatically adding users who register using the front-end form to the 'contributors' group                                  
    """
    if created:
        instance.groups.add(Group.objects.get(name='contributors'))

class Category(models.Model):
    """ Categories are the site sections i.e. the global navigation """
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Suggested value automatically generated from title. Must be unique.")
    description = models.TextField(help_text='Use <a href="/markdown/" onclick="window.open(this.href, this.target); return false;">Markdown format</a>')
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
    """ Live and For Review resource status """
    def get_query_set(self):
        return super(LiveResourceManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

# todo - better file storage:
# http://stackoverflow.com/a/1190866/412329
# def content_file_name(instance, filename):
    # return '/%Y/%m/'.join(['content', instance.user.username, filename])

class Resource(models.Model):
    """ Phytosanitary Resource """
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
    title = models.CharField(unique_for_date='pub_date', blank=False, max_length=250)
    # excerpt = models.TextField(blank=True)
    body = models.TextField(blank=False, help_text='Use <a href="/markdown/" onclick="window.open(this.href, this.target); return false;">Markdown format</a>', verbose_name='Description')
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name='Publication Date', help_text='(will only be published when approved by an administrator)')
    org_title = models.CharField(blank=True, max_length=250, help_text='', verbose_name='Organization')

    url = models.URLField(blank=True, help_text="A link to something elsewhere.", verbose_name='URL')
    contact_type = models.CharField(blank=True, max_length=1, choices=CONTACT_TYPE_CHOICES, default=1, verbose_name='Type of Contact')
    contact_email = models.EmailField(blank=True, verbose_name='Email of Contact')
    contact_address = models.TextField(blank=True, verbose_name='Author/Editor name and address')
    agreement = models.BooleanField(blank=False, verbose_name='Agreed to have these Phytosanitary Technical Resources published in public')
    ippc_resource = models.BooleanField(default=False, verbose_name='Resource provided by the IPPC')

    # Fields to store generated HTML.
    # excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # Metadata.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    # is_homepage = models.BooleanField(default=False)
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
        if not self.slug:
            self.slug = slugify(self.title)
        super(Resource, self).save(force_insert, force_update)
    
    @models.permalink
    def get_absolute_url(self):
        return ('phytosanitary_resource_detail', (), {  'year': self.pub_date.strftime("%Y"),
                                                'month': self.pub_date.strftime("%b").lower(),
                                                'day': self.pub_date.strftime("%d"),
                                                'slug': self.slug })

    # Display filename in templates - http://stackoverflow.com/a/2683834/412329
    def filename(self):
        return os.path.basename(self.document.name)

# tagging users django-tagging
# See http://blog.sveri.de/index.php?/archives/139-django-tagging.html
# With bugfix workaround - http://stackoverflow.com/questions/6295104/django-tagging-already-registered-exception
try:
    tagging.register(Resource, tag_descriptor_attr='etags')
except tagging.AlreadyRegistered:
    pass

class Document(models.Model):
    """ Documents """
    resource = models.ForeignKey(Resource) # , related_name='photos'
    # http://stackoverflow.com/a/1190866/412329
    document = models.FileField(blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/%Y/%m/%d/')

    # Eureka!! http://scottbarnham.com/blog/2008/02/24/imagefield-and-edit_inline-revisited/   
    def save(self):
        if not self.id and not self.document:
            return
        # if self.remove:
        #     self.delete()
        else:
            super(Document, self).save()

    # class Meta:
        # ordering = ['']

    def __unicode__(self):
        return self.document.name

    # http://stackoverflow.com/questions/2683621/django-filefield-return-filename-only-in-template
    def filename(self):
           return os.path.basename(self.document.name)

    # @models.permalink
    # def get_absolute_url(self):
    #     return ('phytosanitary_resource_detail', None, {'object_id': self.id})

class Photo(models.Model):
    """ Photos """
    resource = models.ForeignKey(Resource) # , related_name='photos'
    image = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/") 
    caption = models.CharField(blank=True, max_length=250)

    # Eureka!! http://scottbarnham.com/blog/2008/02/24/imagefield-and-edit_inline-revisited/   
    def save(self):
        if not self.id and not self.image:
            return
        # if self.remove:
        #     self.delete()
        else:
            super(Photo, self).save()
            
    # class Meta:
        # ordering = ['']

    def __unicode__(self):
        return self.image.name
    
    # @models.permalink
    # def get_absolute_url(self):
    #     return ('phytosanitary_resource_detail', None, {'object_id': self.id})


from django import forms
from django.forms import ModelForm, Textarea
class ResourceForm(forms.ModelForm):
    agreement = forms.BooleanField(required=True, label='I agree to have these Phytosanitary Technical Resources published in public')
    
    required_css_class = 'required'
    class Meta:
        model = Resource # model has a user field
        fields = ('title', 'body', 'categories', 'org_title', 'url', 'contact_type', 'contact_email', 'contact_address', 'agreement')
        widgets = {
                    'body': Textarea(attrs={'cols': 80, 'rows': 25})
                }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'caption',)
        exclude = ('resource',)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
        exclude = ('resource',)