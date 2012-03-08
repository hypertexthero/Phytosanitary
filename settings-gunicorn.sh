#!/usr/bin/env python
# filename: gunicorn.sh
# simon’s wrapper for monit fun

export python=/usr/bin/python26
gunicorn_django --bind localhost:8000 --pid /tmp/django-gunicorn-phytosanitary.pid --daemon
echo $!  >  /tmp/django-gunicorn-phytosanitary.pid
 # `$!` Holds the pid of the previously executed process

# command to reload gunicorn: 
# kill -HUP `cat /tmp/django-gunicorn-phytosanitary.pid`

# command to see what gunicorn processes are running
# ps aux | grep gunicorn

# http://www.lifelinux.com/how-to-install-monit-on-centos-redhat/
# The key thing is that you need to output the current process pid to a file when you start django. Monit checks the number in that file to see if there is a living process that matches that number. If not, monit starts the application again. Something like the above will do the trick.
 

 


