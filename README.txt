391_project
===========
Django Photo-Sharing Web Application for CMPUT 391


django Installation
===
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


postgres installation
===
1. After installing python3, and django install the psycopg2 library first.
Use the command: $ pip3 install psycopg2

2. Install postgres.
Note on a Mac use the following link: http://postgresapp.com/. This package will install postgres with all the extra dependancies.

Extra step. In your home directory add this line in the .bashprofile file:
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.3/bin

This allows you to launch psql in terminal.

Otherwise install postgres using pip3 or apt-get, etc depending on the system

3. Create the database and set the following settings using the terminal commands:

We named our db eikon for the greek word for icon
$ createdb eikon

Alternatively: Intitalize psql. Use this cheatsheet to help (https://manikandanmv.wordpress.com/tag/basic-psql-commands/)

Note: The psql terminal interface won't echo after each line. You can enter multi line queries/commands that temrinate with a \ or ;.
If a command doesn't seem to be working break the command with a ; and try again.

#= CREATE ROLE django LOGIN password 'admin';
#= CREATE DATABASE eikon ENCODING 'UTF8' OWNER django;


In settings.py in project_391 change the following line of code with this:

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'eikon', # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'django',
            'PASSWORD': 'admin',
            'HOST': 'localhost', # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '', # Set to empty string for default.
    }
}

References:
1. Tutorial resource (https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn)
2. Stackover Flow Troubleshooting Guide (http://stackoverflow.com/questions/5394331/how-to-setup-postgresql-database-in-django)
3. psql cheatsheet (https://manikandanmv.wordpress.com/tag/basic-psql-commands/)
4. Configure psql and posgres (http://stackoverflow.com/questions/1471571/how-to-configure-postgresql-for-the-first-time)


Queries
===
Modify where necessary (i.e. if we don't need 'X' field, just delete those select statements)

1. Ranking

SELECT photoID,
       OwnerName,
       Permitted
       Subject,
       Place,
       Description,
       Thumbnail,
       Photo,
       ts_rank( array[0.0, 0.1, 0.3, 0.6], img_search.document, to_tsquery('{1}') ) as Rank

FROM ( SELECT images.photo_id as photoID,
              images.owner_name as OwnerName,
              images.permitted as Permitted,
              images.subject as Subject,
              images.place as Place,
              images.description as description,
              images.thumbnail as Thumbnail,
              images.photo as Photo,
              setweight(to_tsvector(images.subject), 'A') ||
              setweight(to_tsvector(images.place), 'B') ||
              setweight(to_tsvector(images.description), 'C')  as document
       FROM images, group_lists
       WHERE  images.permitted = 1 
              OR (images.permitted = 2 AND images.owner_name = '{0}') 
              OR (images.permitted = group_lists.group_id AND group_lists.friend_id = '{0}') ) img_search 
WHERE img_search.document @@ to_tsquery('{1}')
ORDER BY Rank DESC;

2. Date
SELECT images.photo_id,
       images.owner_name,
       images.permitted,
       images.subject,
       images.place,
       images.description,
       images.thumbnail,
       images.photo
FROM images, group_lists
WHERE  images.permitted = 1 
       OR (images.permitted = 2 AND images.owner_name = '{0}') 
       OR (images.permitted = group_lists.group_id AND group_lists.friend_id = '{0}')  
ORDER BY images.timing ASC;

Adjust timing by DESC or ASC where necessary.

Resources, References, and Links
===
. Postgres Setup in Django framework provided by Juan Pablo Arriagada Cancino (http://stackoverflow.com/questions/5394331/how-to-setup-postgresql-database-in-django)
. Postgres psql commands (https://manikandanmv.wordpress.com/tag/basic-psql-commands/)
. CCS Centering solution provided by Billbad (https://stackoverflow.com/questions/396145/how-to-vertically-center-a-div-for-all-browsers). The use of inner, middle, and outer was used to dynamically center elements of HTML sites