# Phytosanitary

Hacking [django-coltrane](http://www.gyford.com/phil/writing/2010/01/14/django.php) to create a generic resources website CMS for my place of work.

## Todo

1. Rename 'Coltrane' to 'Phytosanitary' and…
2. Rename 'Entry' to 'Resource' and…
3. Add relevant fields to 'Resource' and migrate
    - files
    - images
    - modified_date
    - etc
4. User Registration (done?)
    - Non-staff users who register can only submit resources for approval, not publish directly to the site
    - Email notification to moderators/staff when new resources are submitted for approval
5. Editable user profiles for all user types
6. Permissions groups for contributors, moderators, staff
7. Resource publication moderation
8. Implement search of title, body and tag fields at least
9. Currently selected tag and categories should be highlighted in tag and category menus
10. Set up authentication on existing user database backend
11. Implement Internal/External Projects Database with Google map or point to existing Typo3 implementation
12. Implement Markdown preview with WMD
13. Write deployment documentation