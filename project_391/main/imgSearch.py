from django.db import models, connection

def searchImageByText(user, textquery):
    # Submits the raw query into our django db to pull images based on a rank
    # search of the text using lexiemes.
    # Returns all fields to use on the view side.

    dbquery = """
                    SELECT photoID,
                           OwnerName,
                           Permitted,
                           Subject,
                           Place,
                           Timing,
                           Description,
                           Thumbnail,
                           Photo,
                           ts_rank( array[0.0, 0.1, 0.3, 0.6], img_search.document, to_tsquery('{1}') ) as Rank

                    FROM ( SELECT images.photo_id as photoID,
                                  images.owner_name as OwnerName,
                                  images.permitted as Permitted,
                                  images.subject as Subject,
                                  images.timing as Timing,
                                  images.place as Place,
                                  images.description as Description,
                                  images.thumbnail as Thumbnail,
                                  images.photo as Photo,
                                  setweight(to_tsvector(images.subject), 'A') ||
                                  setweight(to_tsvector(images.place), 'B') ||
                                  setweight(to_tsvector(images.description), 'C')  as document
                           FROM images, group_lists
                           WHERE  images.permitted = 1 
                                  OR (images.permitted = 2 AND images.owner_name = '{0}') 
                                  OR (images.permitted = group_lists.group_id AND group_lists.friend_id = '{0}' ) ) img_search 
                    WHERE img_search.document @@ to_tsquery('{1}')
                    ORDER BY Rank DESC;"""
    dbquery = dbquery.format(user.username, textquery)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result = cursor.fetchall()
    return result
    

def searchImageByDate(user='testuser', condition=''):
    if condition == "Newest":
        dbquery = """
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
                    ORDER BY images.timing DESC; """
    else:
        dbquery = """
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
                    ORDER BY images.timing ASC; """

    dbquery.format(user)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    results = cursor.fetchall()
    return results

