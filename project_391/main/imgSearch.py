from django.db import models, connection

def searchImageByText(user='testuser', textquery='lies'):
    # Submits the raw query into our django db to pull images based on a rank
    # search of the text using lexiemes.

    # Ranking formula

    # TODO: Currently outputs photoid. Adjust query to fit Jon's query request
    dbquery = """
                    SELECT thumbnail
                    FROM ( SELECT images.subject,
                                  images.place,
                                  images.description,
                                  images.photo_id as thumbnail,
                                  images.permitted,
                                  setweight(to_tsvector(images.subject), 'A') ||
                                  setweight(to_tsvector(images.place), 'B') ||
                                  setweight(to_tsvector(images.description), 'C')  as document
                           FROM images, group_lists
                           WHERE  images.permitted = 1 
                                  OR (images.permitted = 2 AND images.owner_name = '{0}') 
                                  OR (images.permitted = group_lists.group_id AND group_lists.friend_id = '{0}') ) img_search 
                    WHERE img_search.document @@ to_tsquery('{1}')
                    ORDER BY ts_rank( array[0.0, 0.1, 0.3, 0.6], img_search.document, to_tsquery('{1}') ) DESC;"""
    dbquery = dbquery.format(user, textquery)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result_list = []

    # TODO: If Jon requires additional fields modify this result list append
    for row in cursor.fetchall():
        result_list.append(row[0])
    return result_list   


def searchImageByDate(user='testuser', condition='Newest'):
    if condition == "newest":
        dbquery = """
                    SELECT images.photo_id
                    FROM images, group_lists
                    WHERE  images.permitted = 1 
                           OR (images.permitted = 2 AND images.owner_name = '{0}') 
                           OR (images.permitted = group_lists.group_id AND group_lists.friend_id = '{0}')  
                    ORDER BY images.timing DESC; """
    else:
        dbquery = """
                    SELECT images.photo_id
                    FROM images, group_lists
                    WHERE  images.permitted = 1 
                           OR (images.permitted = 2 AND images.owner_name = '{0}') 
                           OR (images.permitted = group_lists.group_id AND group_lists.friend_id = '{0}')  
                    ORDER BY images.timing ASC;"""
    dbquery.format(user)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result_list = []
    for row in cursor.fetchall():
        result_list.append(row[0])
    return result_list

