from . import kisan

from models import *
from flask import jsonify, request

@kisan.route('/',methods=['GET'])
def basic():
    return jsonify({"response" : "Welcome to Kisan"})
# --------------------------------------------------------- ADD API'S -------------------------------------------------------------------

@kisan.route('/add_person',methods=['POST'])
def add_person() :
    res = request.get_json()
    try :
        person = Person()
        person.import_data(res)
        db.session.add(person)
        db.session.commit()
        print res
        return jsonify({"response" : "success"})
    except Exception as e :
        print str(e)
        db.session.rollback()
        return jsonify({"response" : "Failure", "error" : str(e)})

@kisan.route('/add_address',methods=['POST'])
def add_address():
    res = request.get_json()
    try:
        address = Person_address()
        check = Person.query.get(res['person_id'])
        if check is None:
            return jsonify({"response":"failure","error":"INVALID/INCORRECT ID"})
        address.import_data(res)
        db.session.add(address)
        db.session.flush()
        check.import_address_id(address.id)
        db.session.commit()
        return jsonify({"response":"success"})
    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"response":"failure","error":str(e)})

@kisan.route('/add_images', methods=['POST'])
def add_images():
    res = request.get_json()
    try :
        images = Images()
        images.import_data(res)
        check = Person.query.get(res['person_id'])
        if check is None:
            return jsonify({"response" : "failure", "error" : "add person first"})
        db.session.add(images)
        db.session.commit()
        return jsonify({"response": "success"})
    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"response": "failure", "error": str(e)})

@kisan.route('/add_machinery_to_person',methods=['POST'])
def add_machinery_to_person():
    res = request.get_json()
    try:
        check  = Machinery.query.get(res['company_id'])
        if check is None:
            return jsonify({"response": "failure","error":"INVALID/INCORRECT company ID"})
        check.set_person_id(res['person_id'])
        db.session.commit()
        return jsonify({"response":"success"})

    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"response":"failure","error":str(e)})


@kisan.route('/add_machinery',methods=['POST'])
def add_machinery():
    res = request.get_json()
    try:
        machinery = Machinery()
        machinery.import_data(res)
        check = Company.query.get(res['company_id'])
        if check is None :
            return jsonify({"response" : "failure","error" : "add person first"})
        db.session.add(machinery)
        db.session.commit()
        return jsonify({"response":"success"})
        
    except Exception as e :
        print str(e)
        db.session.rollback()
        return jsonify({"response" : "failure","error" : str(e)})

@kisan.route('/add_company',methods=['POST'])
def add_company():
    res = request.get_json()
    try:
        company = Company()
        company.import_data(res)
        db.session.add(company)
        db.session.commit()
        return jsonify({"response":"sucess"})
    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})

@kisan.route('/add_field',methods=['POST'])
def add_field():
    res = request.get_json()
    try:
        field = Field()
        check = Person.query.get(res['person_id'])
        if check is None:
            return jsonify({"response":"failure","error":"INCORRECT/INVALID Person ID"})
        field.import_data(res)
        db.session.add(field)
        db.session.commit()
        return jsonify({"response": "success"})
    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"response":"failure","error": str(e)})

@kisan.route('/add_Policy',methods=['POST'])
def add_Policy():
    res = request.get_json()
    try:
        policy = Policy()
        check = Company.query.get(res['Company_id'])
        if check is None:
            return jsonify({"response":"failure","error":"INCORRECT/INVALID Company_id"})
        policy.import_data(res)
        db.session.add(policy)
        db.session.commit()
        return jsonify({"response":"success"})
    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"response":"failure","error":str(e)})


# ---------------------------------------------------------------  GET API'S -------------------------------------------------------------------------

@kisan.route('/get_person_details',methods=['GET'])
def get_person_details():
    id = request.args['id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "dob": "",
                "gender": "",
                "phone_no": "",
                "email_id": ""
            }
        }
        person = Person.query.get(id)
        if person is None:
            return jsonify({"response":"failure","error":"No such person with this id"})
        fill_details = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        details = {}
        for key in fill_details :
            details[key] = getattr(person,key)
        return jsonify({"response": "success","data":details})
    except Exception as e:
        print str(e)
        return jsonify({"response": "failure","error":str(e)})


@kisan.route('/get_person_detail_with_images',methods=['GET'])
def get_person_with_images():
    person_id = request.args['person_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "dob": "",
                "gender": "",
                "phone_no": "",
                "email_id": ""
            },
            "IMAGE_LIST": {
                "id": "",
                "image_url": ""
            }
        }
        person = Person.query.get(person_id)
        if person is None:
            return jsonify({"response":"failure","error":"INVALID/INCORRECT ID"})

        details = {}
        details['image_data'] = []
        settings = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        image_settings = TEMP_API_PARAMETERS['IMAGE_LIST']
        for key in settings:
            details[key] = getattr(person,key)

        image_data = Images.query.filter(Images.person_id == person.id)

        for image in image_data:
            if image is not None:
                temp_data = {}
                for key in image_settings:
                    temp_data[key] = getattr(image,key)
                details['image_data'].append(temp_data)

        return jsonify({"response":"success","data":details})

    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"response":"failure","error":str(e)})

@kisan.route('/get_person_fields',methods=['GET'])
def get_person_fields():
    id = request.args['person_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "area": "",
                "price_sqft": "",
                "annual_incg": "",
                "crops_g": ""
            }
        }
        setting = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        person_details = Person.query.get(id)
        if person_details is None:
            return jsonify({"response":"failure","error":"INVALID/INCORRECT PERSON ID"})
        details = []
        fields_list = Field.query.filter(person_details.id == Field.person_id)
        for list in fields_list:
            if list is not None:
                temp = {}
                for key in setting:
                    temp[key]=getattr(list,key)
                details.append(temp)

        return jsonify({"response":"success","data":details})
    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})

@kisan.route('/get_person_details_with_fields',methods=['GET'])
def get_person_details_with_fields():
    id = request.args['person_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "dob": "",
                "gender": "",
                "phone_no": "",
                "email_id": ""
            },
            "FIELDS" : {
                "area": "",
                "price_sqft": "",
                "annual_incg": "",
                "crops_g": ""
            }
        }
        person_setting = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        person_details = Person.query.get(id)
        fields_settings = TEMP_API_PARAMETERS['FIELDS']
        if person_details is None:
            return jsonify({"response":"failure","error":"INVALID/INCORRECT ID"})
        details = {}
        details['fields']=[]
        for key in person_setting:
            details[key]=getattr(person_details,key)
        field_list = Field.query.filter(Field.person_id == id)

        for list in field_list:
            if list is not None:
                temp = {}
                for key in fields_settings:
                    temp[key]=getattr(list,key)
                details['fields'].append(temp)

        return jsonify({"response":"success","data":details})
    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})


@kisan.route('/get_person_details_with_address',methods=['GET'])
def get_person_with_address():
    person_id = request.args['person_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "dob": "",
                "gender": "",
                "phone_no": "",
                "email_id": ""
            },
            "ADDRESS": {
                "home_address": "",
                "district": "",
                "state": "",
                "pincode": ""
            }
        }

        person_settings = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        person_details = Person.query.get(person_id)
        if person_details is None:
            return jsonify({"response":"failure","error":"INVALID/INCORRECT PERSON ID"})
        address_settings = TEMP_API_PARAMETERS['ADDRESS']
        details = {}
        details['address']={}
        for key in person_settings:
            details[key] = getattr(person_details,key)


        address_details = Person_address.query.get(person_details.address_id)
        if address_details is not None:
            print "hello"
            for key in address_settings:
                details['address'][key] = getattr(address_details,key)

        return jsonify({"response":"success","data":details})

    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})


@kisan.route('/get_person_image',methods=['GET'])
def get_person_image():
    id = request.args['id']
    try :
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                    "image_url": "",
                    "id": ""

            }
        }
        check = Person.query.get(id)
        request_details = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        if check is None:
            return jsonify({"response":"failure","error":"no such person with this id"})
        data = []
        image_data = Images.query.filter(Images.person_id == id)
        for key in image_data:
            temp_images = {}
            if key is not None:
                for tt in request_details:
                    temp_images[tt] = getattr(key,tt)
                data.append(temp_images)
        return jsonify({"response": "success", "data":data})
    except Exception as e :
        print str(e)
        return jsonify({"response": "failure","error":str(e)})

@kisan.route('/get_company_details',methods=['GET'])
def get_company_details():
    id = request.args['company_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "location": "",
                "emi": "",
                "rate_int": "",
                "Contact_no": ""
            }
        }

        settings = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        check = Company.query.get(id)
        if check is None :
            return jsonify({"response":"failure","error":"INVALID/INCORRECT COMPANY ID"})
        detail = {}
        for key in settings:
            detail[key] = getattr(check,key)
        return jsonify({"response":"success","data":detail})

    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})

@kisan.route('/get_machine_by_person',methods=['GET'])
def get_machine_by_person():
    id = request.args['person_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "weight": "",
                "stock": "",
                "price": "",
                "spec": "",
                "Date_mfg": "",
                "warranty": "",
            }
        }
        setting = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        check = Person.query.get(id)
        if check is None:
            return jsonify({"response":"failure","error":"INVALID/INCORRECT PERSON ID"})
        details = []
        machine_list = Machinery.query.filter(Machinery.person_id == id)

        for list in machine_list:
            temp = {}
            if list is not None:
                for key in setting:
                    temp[key] = getattr(list,key)

        return jsonify({"response":"success","data":details})

    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})

@kisan.route('/get_company_with_machinery',methods=['GET'])
def get_company_with_machiney():
    id  = request.args['company_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "location": "",
                "emi": "",
                "rate_int": "",
                "Contact_no": ""
            },
            "MACHINERY_DETAILS": {
                "name": "",
                "weight": "",
                "stock": "",
                "price": "",
                "spec": "",
                "warranty": "",
            }
        }
        company = Company.query.get(id)
        if company is None :
            return jsonify({"response": "failure","error":"INVALID/INCORRECT COMPANY ID"})

        setting = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        machine_settings = TEMP_API_PARAMETERS['MACHINERY_DETAILS']
        details = {}
        details['Machines'] = []
        for key in setting:
            details[key] = getattr(company,key)
        machine_list = Machinery.query.filter(company.id == Machinery.company_id)
        for list in machine_list:
            if list is not None:
                temp = {}
                for key in machine_settings:
                    temp[key] = getattr(list,key)
                details['Machines'].append(temp)

        return jsonify({"response":"success","data":details})

    except Exception as e:
        print str(e)
        return jsonify({"response":"error","error":str(e)})

@kisan.route('/get_policy',methods = ['GET'])
def get_policy():
    id = request.args['company_id']
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSE": {
                "name": "",
                "location": "",
                "emi": "",
                "rate_int": "",
                "Contact_no": ""
            },
            "POLICY_DETAILS": {
                "type": "",
                "maturity_period": "",
                "amtdeposited": "",
                "rate": "",
                "documents_reqd": "",
            }

        }
        company = Company.query.get('id')
        if company is None:
            return jsonify({"response": "failure","error":"INVALID/INCORRECT COMPANY ID"})
        settings = TEMP_API_PARAMETERS['SEARCH_RESPONSE']
        policy_settings = TEMP_API_PARAMETERS['POLICY_DETAILS']
        details = {}
        details['policy'] =[]
        for key in settings:
            details[key]=getattr(company,key)
        policy_list  = Policy.query.filter(Policy.company_id == company.id)
        for key in policy_list:
            if key is not None:
                temp = {}
                for key1 in policy_settings:
                    temp[key1] = getattr(key.key1)
                details['policy'].append(temp)

        return jsonify({"response": "success", "data": details})
    except Exception as e:
        print str(e)
        return jsonify({"response":"error","error":str(e)})