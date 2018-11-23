'''class Task(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'email', 'password'):
            setattr(self, field, kwargs.get(field, None))


import psycopg2
class Task(object):
    def __init__(self, **kwargs):
        db = psycopg2.connect(host='localhost', user='username', password='your_password', dbname='your_dbname')
        cursor = db.cursor()
        sql = "show columns from login_table;"
        fields = []
        cursor.execute(sql)
        data = (cursor.fetchall())
        for row in data:
            fields.append(row[0])
        tuple_fields = tuple(fields)
        db.commit()
        db.close()
        for field in tuple_fields:
            setattr(self, field, kwargs.get(field, None))'''
