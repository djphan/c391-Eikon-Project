from django.db import models, connection
def generateDataCube()):
    dbquery = """
              """ 

    dbquery = dbquery.format(user.username, textquery)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result = cursor.fetchall()
    return result


SELECT owner_name, subject, timing, count(*) as image_count FROM Images GROUP BY owner_name, subject, timing
UNION
SELECT owner_name, subject, timing, count(*) as image_count FROM Images GROUP BY owner_name, subject
union 
select null, subject, count(*) from images group by subject;