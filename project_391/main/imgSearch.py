from django.db import models, connection

def DateRangeQueryMaker(startDate, endDate):
    if (startDate == None) & (endDate == None):
        return ""
    elif (startDate == None) & (endDate != None):
        return """AND (img_search.Timing =< '{0}')""".format(str(endDate))
    elif (startDate != None) & (endDate == None):
        return """AND (img_search.Timing >= '{0}') """.format(str(startDate))
    else:
        return """AND ('{0}' <= img_search.Timing) AND (img_search.Timing <= '{1}') """.format(str(startDate), str(endDate))


def searchImageByText(user, textquery, search_start_date, search_end_date):
    # Submits the raw query into our django db to pull images based on a rank
    # search of the text using lexiemes.
    # Returns all fields to use on the view side.

    date_rangeQuery = DateRangeQueryMaker(search_start_date, search_end_date)
    dbquery = """
                    SELECT DISTINCT photoID,
                           OwnerName,
                           Permitted,
                           Subject,
                           Place,
                           Timing,
                           Description,
                           Thumbnail,
                           Photo,
                           ts_rank( array[0.0, 0.1, 0.3, 0.6], img_search.document, to_tsquery(%(query)s)) as Rank
                    FROM ( SELECT images.photo_id as photoID,
                                  images.owner_name as OwnerName,
                                  images.permitted as Permitted,
                                  images.subject as Subject,
                                  images.timing as Timing,
                                  images.place as Place,
                                  images.description as Description,
                                  images.thumbnail as Thumbnail,
                                  images.photo as Photo,
                                  setweight(to_tsvector(coalesce(images.subject, '')), 'A') ||
                                  setweight(to_tsvector(coalesce(images.place, '')), 'B') ||
                                  setweight(to_tsvector(coalesce(images.description, '')), 'C')  as document
                           FROM images, groups, group_lists 
                           WHERE  (images.permitted = 1) 
                                  OR (images.permitted = 2 AND images.owner_name = %(user)s)
                                  OR (images.permitted = groups.group_id AND groups.user_name = %(user)s)
                                  OR (images.permitted = group_lists.group_id AND group_lists.friend_id = %(user)s ) 
                                  %(daterange)s ) img_search 
                    WHERE img_search.document @@ to_tsquery(%(query)s)
                    ORDER BY Rank DESC;"""
    a = """
                    SELECT DISTINCT photoID,
                           OwnerName,
                           Permitted,
                           Subject,
                           Place,
                           Timing,
                           Description,
                           Thumbnail,
                           Photo,
                           ts_rank( array[0.0, 0.1, 0.3, 0.6], img_search.document, to_tsquery('{1}')) as Rank
                    FROM ( SELECT images.photo_id as photoID,
                                  images.owner_name as OwnerName,
                                  images.permitted as Permitted,
                                  images.subject as Subject,
                                  images.timing as Timing,
                                  images.place as Place,
                                  images.description as Description,
                                  images.thumbnail as Thumbnail,
                                  images.photo as Photo,
                                  setweight(to_tsvector(coalesce(images.subject, '')), 'A') ||
                                  setweight(to_tsvector(coalesce(images.place, '')), 'B') ||
                                  setweight(to_tsvector(coalesce(images.description, '')), 'C')  as document
                           FROM images, groups, group_lists 
                           WHERE  (images.permitted = 1) 
                                  OR (images.permitted = 2 AND images.owner_name = '{0}')
                                  OR (images.permitted = groups.group_id AND groups.user_name = '{0}')
                                  OR (images.permitted = group_lists.group_id AND group_lists.friend_id = '{0}')) img_search 
                    WHERE img_search.document @@ to_tsquery('{1}')
                          {2}
                    ORDER BY Rank DESC;"""
    a = a.format(str(user.username), str(textquery), str(date_rangeQuery))
    cursor = connection.cursor()
    cursor.execute(a)
    #cursor.execute(dbquery, {'query':textquery, 'user':user.username, 'daterange':date_rangeQuery})
    result = cursor.fetchall()
    print(result)
    return result



