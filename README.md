# Phytosanitary

Hacking [django-coltrane](http://www.gyford.com/phil/writing/2010/01/14/django.php) to create a generic resources website CMS for my place of work.

## Todo

1. Resource publication [moderation](https://github.com/dominno/django-moderation#readme) - <del>permissions Groups for contributors, moderators, secretariat staff</del> _done_
    - Non-secretariat users who register can only submit resources for approval by a moderator or chief administrator, not publish directly to the site.
        - <del>[Users who register through front-end of site need to be automatically assigned to 'contributors' group](http://stackoverflow.com/questions/8949303/how-to-assign-a-user-to-a-group-at-signup-using-django-userena)</del> Done.
        - *Contributors can add/save a resource with [For Review](http://collingrady.wordpress.com/2008/07/24/useful-form-tricks-in-django/) status only*
    - [Email](http://stackoverflow.com/questions/2349483/django-models-signals-and-email-sending-delay) [notification](https://github.com/jtauber/django-notification/) [to](https://docs.djangoproject.com/en/dev/topics/email/) moderators/staff when new resources are submitted
2. Create contributor resource upload form with the following fields:
    - title - text
    - date of publication - YYYY Month DD select menu or calendar widget
    - description - textarea
    - authors/editors - text
    - title of organization - text
    - file upload - file
    - url - text
    - contact type - radio: rppo, nppo, other. if other: text
    - email - input
    - address of contact - textarea
    - phytosanitary resource type ([tags](https://github.com/brosner/django-tagging/blob/master/docs/overview.txt#L701)) - checkbox or text with anchor list
    - Do you agree to have these Phytosanitary Technical Resources published in public? - checkbox
3. <del>Search</del>. Done, but debug the error when using named url in search.html
4. Currently selected tag should be highlighted in Browse Tags menu
5. Markdown WYSIWYG with WMD
6. Set up and document deployment to production server
7. Set up authentication on existing user database backend
8. Implement Internal/External Projects Database with Google map or point to existing Typo3 implementation
9. [Set up fixtures](fixtures) for Categories, Tags and Sitename to be automatically added to the database upon installation. Also update tagging
10. Change banner design and colors
11. Syndication feeds


### Future

- Custom application page pulling data from an external source using something like the [infochimps apis](http://www.infochimps.com/datasets/plant-pest-risk-analyses-pra-documents#overview_tab) (thanks B.B.King of *x sysadmin)
- I18N, including right-to-left scripts such as Arabic

### Upcoming advantages of the new django-powered website

- Faster (less database queries)
- Clean URLs!
- Easy to add and edit articles (human-writeable and readable Markdown syntax)
- You get redirected to the URL you wanted to reach after logging in
- Clean HTML templates
- Permissions groups for contributors, secretariat staff, superadmins

[fixtures]: https://docs.djangoproject.com/en/dev/topics/testing/#topics-testing-fixtures