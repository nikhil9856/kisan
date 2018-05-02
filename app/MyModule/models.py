from app import db
from sqlalchemy import event
from app.models import *
from controller import after_entry_insert, after_entry_update


class Person(Base):
    __tablename__ = 'person'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(128),nullable=False)
    dob = db.Column(db.String(128),nullable=False)
    gender = db.Column(db.Enum('M','F'))
    phone_no = db.Column(db.String(16),nullable=False)
    email_id = db.Column(db.String(128),nullable=True)
    address_id = db.Column(db.Integer,db.ForeignKey("person_address.id"))

    def import_data(self,data):
        try:
            self.name = data['name']
            self.dob = data['dob']
            self.gender = data['gender']
            self.phone_no = data['phone_no']
            self.email_id = data.get('email_id',None)
            return self
        except Exception as e:
            return str(e)

    def import_address_id(self,address_id):
        try:
            self.address_id = address_id
            return self
        except Exception as e:
            return str(e)

class Person_address(Base):
    __tablename__ = 'person_address'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    home_address = db.Column(db.String(128), nullable=False)
    district = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(128), nullable=False)
    pincode = db.Column(db.String(128),nullable=False)

    def import_data(self,data):
        try:
            self.home_address = data['home_address']
            self.district = data['district']
            self.state = data['state']
            self.pincode = data['pincode']
            return self
        except Exception as e:
            return str(e)

class Images(Base):
    __tablename__ = 'images'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    image_url = db.Column(db.String(128),nullable=False)

    def import_data(self,data):
        try :
            self.image_url = data['image_url']
            self.person_id = data.get('person_id',None)
            return self
        except Exception as e :
            return str(e)

class Machinery(Base):
    __tablename__ = 'machinery'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    name = db.Column(db.String(128),nullable=False)
    weight = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer,nullable=False)
    spec = db.Column(db.String(128))
    Date_mfg = db.Column(db.Date,nullable=False)
    warranty = db.Column(db.String(128))
    company_id = db.Column(db.Integer,db.ForeignKey("company.id"), nullable=False)

    def import_data(self,data):
        try:
            self.name = data["name"]
            self.weight = data.get("weight",None)
            self.stock = data.get("stock",None)
            self.price = data["price"]
            self.spec = data.get("spec",None)
            self.Date_mfg = data["Date_mfg"]
            self.warranty = data.get("warranty",None)
            self.company_id = data['company_id']
            return self
        except Exception as e:
            return str(e)
    def set_person_id(self,person_id):
        try:
            self.person_id = person_id
            return self
        except Exception as e:
            return str(e)

class Field(Base):
    __tablename__ = 'field'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    person_id = db.Column(db.Integer,db.ForeignKey("person.id"),nullable=False)
    area = db.Column(db.Integer,nullable = False)
    price_sqft = db.Column(db.Integer,nullable = False)
    annual_incg = db.Column(db.Integer,nullable = False)
    crops_g = db.Column(db.String(128),nullable=False)

    def import_data(self,data):
        try:
            self.person_id = data["person_id"]
            self.area = data["area"]
            self.price_sqft = data["price_sqft"]
            self.annual_incg = data["annual_incg"]
            self.crops_g = data["crops_g"]
            return self
        except Exception as e:
            return str(e)

class Company(Base):
    __tablename__ = 'company'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(128),nullable=False)
    estd = db.Column(db.Date,nullable = False)
    location = db.Column(db.String(128),nullable = False)
    emi = db.Column(db.Integer,nullable=False)
    rate_int = db.Column(db.Integer,nullable = False)
    Contact_no = db.Column(db.Integer,nullable= False)

    def import_data(self,data):
        try:
            self.name = data["name"]
            self.estd = data["estd"]
            self.location = data["location"]
            self.emi = data["emi"]
            self.rate_int = data["rate_int"]
            self.Contact_no = data["Contact_no"]
            return self
        except Exception as e:
            return str(e)

class Policy(Base):
    __tablename__ = 'policy'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey("company.id"),nullable=False)
    type = db.Column(db.String(128),nullable=False)
    maturity_period = db.Column(db.Integer)
    documents_reqd = db.Column(db.String(128))
    rate = db.Column(db.Integer,nullable=False)
    amtdeposited = db.Column(db.Integer,nullable=False)

    def import_data(self,data):
        try:
            self.company_id = data["company_id"]
            self.type = data["type"]
            self.maturity_period = data.get("maturity_period",None)
            self.amtdeposited = data.get("amtdeposited",None)
            self.rate = data.get("rate",None)
            self.documents_reqd = data.get("documents_reqd",None)
            return self
        except Exception as e:
            return str(e)
