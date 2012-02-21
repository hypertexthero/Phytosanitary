# Phytosanitary

Hacking [django-coltrane](http://www.gyford.com/phil/writing/2010/01/14/django.php) to create a generic resources website CMS for my place of work.

## Todo

1. Resource publication moderation - permissions Groups for contributors, moderators, secretariat staff
    - Non-secretariat users who register can only submit resources for approval, not publish directly to the site, unless their permissions are changed.
        - [Users who register through front-end of site need to be automatically assigned to 'contributors' group](http://stackoverflow.com/questions/8949303/how-to-assign-a-user-to-a-group-at-signup-using-django-userena)
        - Contributors can add/save a resource as Draft/for review only
    - Email notification to moderators/staff when new resources are submitted
2. Default resource form fields
    - files
    - images
3. Search
4. Set up authentication on existing user database backend
5. Implement Internal/External Projects Database with Google map or point to existing Typo3 implementation
6. Custom application page pulling data from an external source using something like the [infochimps apis](http://www.infochimps.com/datasets/plant-pest-risk-analyses-pra-documents#overview_tab) (thanks B.B.King of *x sysadmin)
7. Currently selected tag should be highlighted in Browse Tags menu
8. Set up and document deployment to production server