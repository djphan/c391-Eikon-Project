from django.db import models
from django.db import connection
from main.imgSearch import searchImageByText, searchImageByDate

# Create your models heres
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

    def search(self, condition):
        return

    class Meta:
        db_table = "persons"

    def __str__(self):
        return ' '.join([str(self.user_name), '-', self.first_name, self.last_name, self.email])


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    user_name = models.ForeignKey(Users, db_column="user_name")
    group_name = models.CharField(max_length=24, db_column="group_name")
    date_created = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = "groups"
        unique_together = (("user_name", "group_name"),)


class GroupLists(models.Model):
    """
    """
    group_id = models.ForeignKey(Groups, db_column="group_id")
    friend_id = models.ForeignKey(Users, db_column="friend_id")
    date_added = models.DateField(auto_now_add=True)
    notice = models.CharField(max_length=1024)

    class Meta:
        db_table = "group_lists"
        unique_together = (("group_id", "friend_id"),)


class Images(models.Model):
    photo_id = models.AutoField(primary_key=True)
    owner_name = models.ForeignKey(Users, db_column="owner_name")
    permitted = models.ForeignKey(Groups, db_column="permitted")
    subject = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    timing = models.DateField(auto_now_add=False)
    description = models.CharField(max_length=2048)
    
    thumbnail = models.ImageField(upload_to="Thumbnails/", max_length=250)
    photo = models.ImageField(upload_to="Images", max_length=250)

    def searchByText(user, textquery):
        import pdb; pdb.set_trace()
        results = searchImageByText(user, textquery)
        search_results = []
        for row in results:
            search_results.append(Images())
            search_results[-1].photo_id=row[0]
            search_results[-1].owner_name=Users.objects.get(username=row[1])
            search_results[-1].permitted=Groups.objects.get(username=row[1], group_id=row[2])
            search_results[-1].subject=row[3]
            search_results[-1].place=row[4]
            search_results[-1].timing=row[5]
            search_results[-1].description=row[6]
            search_results[-1].thumbnail=row[7]
            search_results[-1].photo=row[8]
        return search_results

    class Meta:
        db_table = "images"

    def searchByDate(user='testuser', condition='newest'):
        return searchImageByDate(user, condition)

    def __str__(self):
        return ('ID: photo_id' + ' :: ' + photo)
              
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
