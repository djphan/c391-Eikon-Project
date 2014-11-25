

from django.db import models, connection

def generateDataCube(owner_name=None, subject=None, timing=None):
    if owner_name == None:
        owner_name = 'null'

    if subject == None:
        subject = 'null'

    if timing == None:
        field = 'null'
        timing = 'null'

    elif timing == 'timing':
        field = 'timing'
    else:
        field = timing
        timing = """date_trunc('{0}', timing) as {0} """.format(timing)
      
    if ((owner_name == 'null') & (subject == 'null') & (timing == 'null')):
        dbquery = """
                  SELECT owner_name, subject, timing, count(*) as image_count FROM Images GROUP BY owner_name, subject, timing
                  """ 
    else:    
        dbquery = """
                    SELECT {0}, {1}, {2}, count(*) as image_count FROM Images GROUP BY {0}, {1}, {3};
                  """ 
        dbquery = dbquery.format(owner_name, subject, timing, field)

    print(dbquery)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result = cursor.fetchall()
    return result
