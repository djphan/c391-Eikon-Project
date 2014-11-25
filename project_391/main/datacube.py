from django.db import models, connection

def generateDataCube(owner_name=None, subject=None, timing=None):
    dbquery = "SELECT {0}, {1}, {2}, count(*) FROM images GROUP BY {3};"

    zero = "owner_name" if owner_name else "null"
    one = "subject" if subject else "null"
    two = "timing" if timing else "null"
    three = ""
    if owner_name: three += "owner_name, "
    if subject:    three += "subject, "
    if timing:     three += "timing, "
    if len(three) > 0: three = three[:-2]

    dbquery = dbquery.format(zero, one, two, three)
    if not any([owner_name, subject, timing]):
        dbquery = dbquery[:-11]
    
    print(dbquery)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result = cursor.fetchall()
    
    json = list()

    for db_row in result:
        row = dict()
        if owner_name:
            row["Owner"] = db_row[0]
        if subject:
            row["Subject"] = db_row[1]
        if timing:
            row["Timing"] = db_row[2]
        
        row["Count"] = db_row[3]
        json.append(row)

    return json

# """
# SELECT owner_name, subject, timing, count(*) as image_count FROM Images GROUP BY owner_name, subject, timing
# UNION ALL
# SELECT owner_name, null, timing, count(*) as image_count FROM Images GROUP BY owner_name, timing
# UNION ALL
# SELECT null, subject, timing, count(*) as image_count FROM Images GROUP BY subject, timing
# UNION ALL
# SELECT owner_name, subject, null, count(*) as image_count FROM Images GROUP BY owner_name, subject
# UNION ALL
# SELECT owner_name, null, null, count(*) as image_count FROM Images GROUP BY owner_name
# UNION ALL
# SELECT null, subject, null, count(*) as image_count FROM images GROUP BY subject
# UNION ALL
# SELECT null, null, timing, count(*) as image_count FROM images GROUP BY timing
# UNION ALL
# SELECT null, null, null, count(*) as image_count FROM images;
# """
