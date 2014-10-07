391_project
===========

Django Photo-Sharing Web Application for CMPUT 391


Instructions to set this up on your computer:

(Note: I'm working in Ubuntu 14.04, but hopefully these instructions should be
the same for you. I'm mostly following the beginning of http://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/
here, with a couple alterations that I found were needed for python3)

First make sure you have pip3 installed:
$ pip3 -V
You should get something like this:
pip 1.5.4 from /usr/lib/python3/dist-packages (python 3.4)

If not, google how to install it for your system.

Next:
$ pip3 install virtualenvwrapper

Add the following to your shell's startup file (probably .bashrc):

export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/directory-you-do-development-in
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

Restart your terminal.

Next:
$ mkvirtualenv 391_project

What this does is installs a fresh python and pip that you only use when working
on this project. (You can check this by running "which python". Compare with
other programs you already have installed ("which git" for example): you still
have access to everything else.) From now on if you're working on the project,
make sure you're in the virtualenv.

$ workon 391_project            # to enter virtualenv
$ deactivate                    # to leave virtualenv

Next:

$ pip3 install django

DON'T skip this step. Make sure it worked by running "which django-admin.py" If
the path doesn't contain .../.virtualenv/... then you're running your computer's
version of django, which we don't want to get mixed up with the project's
version.

Finally:
$ pip3 install pillow

At this point you should be able to git clone this repository and run the server.

:-)


The only current superuser is:
username: admin
password: 391foo1
You'll need this to log in to the admin side of the server.
You can add yourselves as superusers too of course.
