from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=24, db_column="user_name")
    password = models.CharField(max_length=24)
    date_registered = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
        

class Persons(models.Model):
    user_name = models.ForeignKey(Users, primary_key=True, db_column="user_name")
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    address = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    phone = models.CharField(max_length=10)

    class Meta:
        db_table = "persons"

    def __str__(self):
        return ' '.join([str(self.user_name), '-', self.first_name, self.last_name, self.email])


class Groups(models.Model):
    group_id = models.IntegerField(primary_key=True)
    user_name = models.ForeignKey(Users, db_column="user_name")
    group_name = models.CharField(max_length=24, db_column="group_name")
    date_created = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = "groups"
        unique_together = (("user_name", "group_name"),)


class GroupLists(models.Model):
    """
    Note: I'm not specifying a primary key here, so Django will automatically
    create its own.  For all intents and purposes we can ignore this column in
    the table.  The reason I'm doing this is Django does not support
    multiple-column "composite" primary keys, as specified in the assignment
    specs. Instead I'll make group_id and friend_id "unique_together", which
    will make them a candidate key for the table. This achieves the same
    behaviour as making them the primary key, so to anyone testing queries on
    our database it will act as expected.

    There may be another way to do this, I will check it out when I have
    time. This'll work for now though :-)
    -Carl
    """
    group_id = models.ForeignKey(Groups, db_column="group_id")
    friend_id = models.ForeignKey(Users, db_column="friend_id")
    date_added = models.DateField(auto_now_add=True)
    notice = models.CharField(max_length=1024)

    class Meta:
        db_table = "group_lists"
        unique_together = (("group_id", "friend_id"),)


class Images(models.Model):
    photo_id = models.IntegerField(primary_key=True)
    owner_name = models.ForeignKey(Users, db_column="owner_name")
    permitted = models.ForeignKey(Groups, db_column="permitted")
    subject = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    timing = models.DateField(auto_now_add=False)
    description = models.CharField(max_length=2048)
    
    # This will create a VARCHAR(100) field which will store the URL of the file
    # I _believe_ once we specify a MEDIA_ROOT settings variable then this will
    # allow Django to store all the files there, but it may be more complicated
    # than that. For now, I'll just have it make the default ImageField so we
    # can use the class/tables in the templates.
    thumbnail = models.ImageField()
    photo = models.ImageField()

    class Meta:
        db_table = "images"


        # TODO: - Dan Implement search query based on ranking system givne in assignment specificiations
        pass

        
class Session(models.Model):
    username = models.ForeignKey(Users)
    sessiontracker = models.IntegerField(primary_key=True)
    # expiry = models.DateField()  # implement later?
    
    
    class Meta:
        db_table = "session"

    def __str__(self):
        # String form is username plus last 4 digits of sessiontracker
        return ("(%s:...%s)"%(self.username.username, str(self.sessiontracker)[-4:]))
