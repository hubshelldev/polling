from apps.phygital_account.models import *
from apps.phygital_admin.models import *

from utils import json as Json
from utils import validators,functions

def school_validations(row_iter):
    error_array = []
    creation_array = []
    remaining_array = []
    for index, row in row_iter:
        error_key=[]
        error_msg=[]
        if row['SCHOOL_NAME']=="":
            text_key = "SCHOOL_NAME"
            error_key.append(text_key)
            text_msg = "school name is missing"
            error_msg.append(text_msg)
        if row['CURRICULAM']=="":
            text_key = "CURRICULAM"
            error_key.append(text_key)
            text_msg = "curriculam is missing"
            error_msg.append(text_msg)
        if row['EMAIL']=="":
            text_key = "EMAIL"
            error_key.append(text_key)
            text_msg = "email is missing"
            error_msg.append(text_msg)
        if row['PHONE_NUMBER']=="":
            text_key = "PHONE_NUMBER"
            error_key.append(text_key)
            text_msg = "Phone number is missing"
            error_msg.append(text_msg)
        if row['ADDRESS']=="":
            text_key = "ADDRESS"
            error_key.append(text_key)
            text_msg = "Address is missing"
            error_msg.append(text_msg)

        result = functions.is_valid_email(row['EMAIL'])
        if result == False:
            text_key = "VALIDE EMAIL"
            error_key.append(text_key)
            text_msg = "Provide valid email"
            error_msg.append(text_msg)
            
        result = functions.is_valid_phone(row['PHONE_NUMBER'])
        if result == False:
            text_key = "VALIDE PHONE_NUMBER"
            error_key.append(text_key)
            text_msg = "Provide valid phone number"
            error_msg.append(text_msg)
        # if User.objects.filter(email=row['EMAIL']).exists():
        #     creation_array.append(dict(row))
        #     text_key = "EMAIL EXIST"
        #     error_key.append(text_key)
        #     text_msg = "Email already exist"
        #     error_msg.append(text_msg)
        if User.objects.filter(phone_number=row['PHONE_NUMBER']).exists():
            text_key = "PHONE_NUMBER EXIST"
            error_key.append(text_key)
            text_msg = "Phone number already exist"
            error_msg.append(text_msg)
        
        if SchoolMaster.objects.filter(school_name=row['SCHOOL_NAME'],email=row['EMAIL'],phone_number=row['PHONE_NUMBER'],is_deleted=False).exists():
            text_key = "SCHOOL NAME EXIST"
            error_key.append(text_key)
            text_msg = "School name already exist"
            error_msg.append(text_msg)
        error_key = ",".join(error_key)
        row['ERROR STATUS'] = error_key
        error_msg = ",".join(error_msg)
        row['ERROR MESSAGE'] = error_msg

        if len(error_key) != 0 or len(error_msg) !=0:
            error_array.append(dict(row))
        else:
            remaining_array.append(dict(row)) 
    return error_array,remaining_array,creation_array