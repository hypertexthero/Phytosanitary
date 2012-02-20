# Phytosanitary

Hacking [django-coltrane](http://www.gyford.com/phil/writing/2010/01/14/django.php) to create a generic resources website CMS for my place of work.

## Todo

1. Rename 'coltrane' to 'phytosanitary'
2. Rename 'entry' to 'resource'
3. -User Registration-
4. -Editable user profiles-
5. Resource publication moderation - permissions Groups for contributors, moderators, secretariat staff
    - Non-secretariat users who register can only submit resources for approval, not publish directly to the site, unless their permissions are changed.
    - Email notification to moderators/staff when new resources are submitted
6. Default resource form fields
    - files
    - images
7. Search
8. Currently selected tag should be highlighted in Browse Tags menu
9. Set up authentication on existing user database backend
10. Implement Internal/External Projects Database with Google map or point to existing Typo3 implementation
11. Custom application page pulling data from an external source using something like the [infochimps apis](http://www.infochimps.com/datasets/plant-pest-risk-analyses-pra-documents#overview_tab) (thanks B.B.King of *x sysadmin)