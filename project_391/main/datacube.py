from django.db import models, connection

def generateDataCube(owner_name=None, subject=None, timing=None):
    if ((owner_name == None) & (subject == None) & (timing == None)):
        dbquery = """
                  SELECT owner_name, subject, timing, count(*) as image_count FROM Images GROUP BY owner_name, subject, timing
                  """ 
    elif timing == 'timing':
        dbquery = """
                    SELECT {0} {1} timing, count(*) as image_count FROM Images GROUP BY {0} {1} timing;
                  """ 
        dbquery = dbquery.format(
                                 '' if owner_name==None else 'owner_name' + '{0}'.format(',' if (subject != None) | (timing != None) else ';'), 
                                 '' if subject==None else 'subject,' 
                                )     

    else:    
        dbquery = """
                    SELECT {0} {1} {2} count(*) as image_count FROM Images GROUP BY {0} {1} {3};
                  """ 
        # Ultra Silly String Formatting
        dbquery = dbquery.format(
                                 '' if owner_name==None else 'owner_name' + '{0}'.format(',' if (subject != None) | (timing != None) else ';'), 
                                 '' if subject==None else 'subject' + '{0}'.format(',' if timing !=None else ';'), 
                                 '' if (timing==None) else  """date_trunc('{0}', timing) as {0}, """.format(timing),
                                 '' if (timing==None) else str(timing)
                                ) 
                 

    print(dbquery)
    cursor = connection.cursor()
    cursor.execute(dbquery)
    result = cursor.fetchall()
    return result
