from django.db import models, connection
def generateDataCube(owner_name, subject, timing):
    if timing == null:
        field = 'timing'
        timing = 'timing'
    else:
        field = timing
        timing = """date_trunc({0}, timing)""".format(timing)


    dbquery = """
                SELECT owner_name, subject, {0}, count(*) as image_count FROM Images GROUP BY owner_name, subject, {1}
                UNION ALL
                SELECT owner_name, null, {0}, count(*) as image_count FROM Images GROUP BY owner_name, {1}
                UNION ALL
                SELECT null, subject, {0}, count(*) as image_count FROM Images GROUP BY subject, {1}
                UNION ALL
                SELECT owner_name, subject, null, count(*) as image_count FROM Images GROUP BY owner_name, subject
                UNION ALL
                SELECT owner_name, null, null, count(*) as image_count FROM Images GROUP BY owner_name
                UNION ALL
                SELECT null, subject, null, count(*) as image_count FROM images GROUP BY subject
                UNION ALL
                SELECT null, null, {0}, count(*) as image_count FROM images GROUP BY {1};
              """ 

    dbquery = dbquery.format(timing, field)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result = cursor.fetchall()
    return result
