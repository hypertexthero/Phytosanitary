# Phytosanitary

Hacking [django-coltrane](http://www.gyford.com/phil/writing/2010/01/14/django.php) to create a generic resources website CMS for my place of work.

## Todo

1. Add ability to [upload multiple files](http://stackoverflow.com/questions/4343413/how-to-upload-multiple-file-in-django-admin-models) per resource
2. Add simple captcha in form of random question/answers?
3. [Email](http://stackoverflow.com/questions/2349483/django-models-signals-and-email-sending-delay) [notification](https://github.com/jtauber/django-notification/) [to](https://docs.djangoproject.com/en/dev/topics/email/) moderators/staff and contributor who uploaded resource when new resources are submitted
4. Set up 'other' text field for phytosanitary resource type
5. Markdown WYSIWYG with WMD for resource descriptions
6. Set up authentication using www.ippc.int existing user database backend.
7. <del>Implement Internal/External Projects Database with Google map or</del> point to existing Typo3 implementation
8. [Set up fixtures](fixtures) for Categories, Tags and Sitename to be automatically added to the database upon installation. Also update tagging
9. Change banner design and colors
10. Document application deployment to production server and update workflow
11. Add photo field with thumbnail display in detail view.
12. Make homepage introduction text editable with Markdown and WMD preview


### Future

- Syndication feeds
- I18N, including right-to-left scripts such as Arabic
- Custom application page pulling data from an external source using something like the [infochimps apis](http://www.infochimps.com/datasets/plant-pest-risk-analyses-pra-documents#overview_tab) (thanks B.B.King of *x sysadmin)
- Currently selected tag should be highlighted in Browse Tags menu

### Upcoming advantages of the new django-powered website

- Faster (less database queries)
- Clean URLs!
- Easy to add and edit articles (human-writeable and readable Markdown syntax)
- You get redirected to the URL you wanted to reach after logging in
- Clean HTML templates
- Permissions groups for contributors, secretariat staff, superadmins

[fixtures]: https://docs.djangoproject.com/en/dev/topics/testing/#topics-testing-fixtures