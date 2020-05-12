from peewee import *

db = SqliteDatabase('deals.db')

class Deal(Model):
    title = CharField()
    url = CharField()
    ident = CharField()
    created = DateTimeField()
    posted = BooleanField()

    class Meta:
        database = db

db.connect()
db.create_tables([Deal])