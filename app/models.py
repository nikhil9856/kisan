
#Add all common models/tables in this file.

from app import db

class Base(db.Model):
    __abstract__ = True
    created_on =      db.Column((db.DateTime))
    updated_by =      db.Column((db.String(64)))
    updated_on =      db.Column((db.DateTime))

