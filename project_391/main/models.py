from django.db import models
from django.db import connection
from main.imgSearch import searchImageByText

# Create your models heres

class SubjectDashboard(models.Model):
    def __str__(self):
        return Images.objects.all().aggregate(Sum('subject'))

class Views(models.Model):
    photo_id = models.ForeignKey('Images', db_column="photo_id")
    user_name = models.ForeignKey('Users', db_column="user_name") 
    class Meta:
        db_table = "views"
        unique_together = (("photo_id", "user_name"),)
        verbose_name = "View"

    def __str__(self):
        return "Image: " + str(self.photo_id.photo_id) + ", Viewer: " + str(self.user_name)

class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=24, db_column="user_name")
    password = models.CharField(max_length=24)
    date_registered = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"

    def __str__(self):
        return "Username: " + self.username + ", Total Images: " + str(Images.objects.filter(owner_name=self).count())
        

class Persons(models.Model):
    user_name = models.ForeignKey(Users, primary_key=True, db_column="user_name")
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    address = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    phone = models.CharField(max_length=20)

    def search(self, condition):
        return

    class Meta:
        db_table = "persons"
        verbose_name = "Person"

    def __str__(self):
        return ' '.join([str(self.user_name), '-', self.first_name, self.last_name, self.email])


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    user_name = models.ForeignKey(Users, db_column="user_name", null=True)
    group_name = models.CharField(max_length=24, db_column="group_name")
    date_created = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = "groups"
        unique_together = (("user_name", "group_name"),)
        verbose_name = "Group"

    def __str__(self):
        return self.group_name

class GroupLists(models.Model):
    """
    """
    group_id = models.ForeignKey(Groups, db_column="group_id")
    friend_id = models.ForeignKey(Users, db_column="friend_id")
    date_added = models.DateField(auto_now_add=True)
    notice = models.CharField(max_length=1024, blank=True)

    class Meta:
        db_table = "group_lists"
        unique_together = (("group_id", "friend_id"),)
        verbose_name = "GroupList"

    def __str__(self):
        return "Group Name: " + str(self.group_id) + " Member Name: " + str(self.friend_id)

class Images(models.Model):
    photo_id = models.AutoField(primary_key=True)
    owner_name = models.ForeignKey(Users, db_column="owner_name")
    permitted = models.ForeignKey(Groups, db_column="permitted")
    subject = models.CharField(max_length=128, blank=True, null=True)
    place = models.CharField(max_length=128, blank=True, null=True)
    timing = models.DateField(auto_now_add=False, blank=True, null=True)
    description = models.CharField(max_length=2048, blank=True, null=True)
    
    thumbnail = models.ImageField(upload_to="Thumbnails/", max_length=250)
    photo = models.ImageField(upload_to="Images", max_length=250)
    
    def searchByText(user, textquery, startDate, endDate):
        results = searchImageByText(user, textquery, startDate, endDate)
        print(len(results))
        search_results = []
        for row in results:
            print(len(row))
            search_results.append(Images())
            search_results[-1].photo_id=row[0]
            search_results[-1].owner_name=Users.objects.get(username=row[1])
            search_results[-1].permitted=Groups.objects.get(group_id=row[2])
            search_results[-1].subject=row[3]
            search_results[-1].place=row[4]
            search_results[-1].timing=row[5]
            search_results[-1].description=row[6]
            search_results[-1].thumbnail=row[7]
            search_results[-1].photo=row[8]
        print(search_results)
        return search_results

    class Meta:
        db_table = "images"
        verbose_name = "Image"

    def searchByDate(user, condition):
        results = searchImageByDate(user, condition)
        print(results)
        search_results = []
        #import pdb
        for row in results:
            #pdb.set_trace()
            search_results.append(Images())
            search_results[-1].photo_id=row[0]
            search_results[-1].owner_name=Users.objects.get(username=row[1])
            search_results[-1].permitted=Groups.objects.get(group_id=row[2])
            search_results[-1].subject=row[3]
            search_results[-1].place=row[4]
            search_results[-1].timing=row[5]
            search_results[-1].description=row[6]
            search_results[-1].thumbnail=row[7]
            search_results[-1].photo=row[8]
        print(search_results)
        return search_results


    def __str__(self):
        return ('ID: photo_id' + ' :: ' + self.photo.url)
              
class Session(models.Model):
    username = models.ForeignKey(Users)
    sessiontracker = models.CharField(max_length=32, primary_key=True)
    # expiry = models.DateField()  # implement later?
    
    
    class Meta:
        db_table = "session"

    def __str__(self):
        # String form is username plus last 4 digits of sessiontracker
        return ("(%s:...%s)"%(self.username.username, str(self.sessiontracker)[-4:]))

        
# /*
#  *  File name:  setup.sql
#  *  Function:   to create the intial database schema for the CMPUT 391 project,
#  *              Fall, 2014
#  *  Author:     Prof. Li-Yan Yuan
#  */
# DROP TABLE images;
# DROP TABLE group_lists;
# DROP TABLE groups;
# DROP TABLE persons;
# DROP TABLE users;


# CREATE TABLE users (
#    user_name varchar(24),
#    password  varchar(24),
#    date_registered date,
#    primary key(user_name)
# );

# CREATE TABLE persons (
#    user_name  varchar(24),
#    first_name varchar(24),
#    last_name  varchar(24),
#    address    varchar(128),
#    email      varchar(128),
#    phone      char(10),
#    PRIMARY KEY(user_name),
#    UNIQUE (email),
#    FOREIGN KEY (user_name) REFERENCES users
# );


# CREATE TABLE groups (
#    group_id   int,
#    user_name  varchar(24),
#    group_name varchar(24),
#    date_created date,
#    PRIMARY KEY (group_id),
#    UNIQUE (user_name, group_name),
#    FOREIGN KEY(user_name) REFERENCES users
# );

# INSERT INTO groups values(1,null,'public', sysdate);
# INSERT INTO groups values(2,null,'private',sysdate);

# CREATE TABLE group_lists (
#    group_id    int,
#    friend_id   varchar(24),
#    date_added  date,
#    notice      varchar(1024),
#    PRIMARY KEY(group_id, friend_id),
#    FOREIGN KEY(group_id) REFERENCES groups,
#    FOREIGN KEY(friend_id) REFERENCES users
# );

# CREATE TABLE images (
#    photo_id    int,
#    owner_name  varchar(24),
#    permitted   int,
#    subject     varchar(128),
#    place       varchar(128),
#    timing      date,
#    description varchar(2048),
#    thumbnail   blob,
#    photo       blob,
#    PRIMARY KEY(photo_id),
#    FOREIGN KEY(owner_name) REFERENCES users,
#    FOREIGN KEY(permitted) REFERENCES groups
# );
