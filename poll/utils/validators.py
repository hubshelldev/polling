"""
Email login validators
"""
from utils import functions
import json as j
from decimal import Decimal

from apps.employee.models import *

def Email_login_validators(data):
    try:
        json_keys =['email','password']
        json_values =['email','password']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_values:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
            if val=='email':            
                result = functions.is_valid_email(data[val])
                if result == False:
                    return {'data':"please enter a valid email address",'status':False}
            if val=='password':            
                result = functions.is_valid_password(data[val])
                if result == False:
                    return {'data':"please enter a valid password",'status':False}
            
        return {'status': True}

    except Exception as e:
        return {'data':e+"Internal Error",'status':False}

""" 
resetpassword validators 
"""
def Resetpassword_validators(data):
    try:
        json_keys=['password','confirm_password','uid','token']
        
        for key in json_keys:
            if key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_keys:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
            
            if val=='password':                      
                if len(data[val])<8:
                    return {'data':"Password minimum should be 8 characters",'status':False}
                else:
                    result = functions.is_valid_password(data[val])
                    if result == False:
                        return {'data':"Password should contain at least one numeric character and one special character and one upper case ",'status':False}
    
    
    except Exception as e:
       return {'data':e+"Internal Error",'status':False}

""" 
update password validator
"""
def Updatepassword_validator(data):
    try:
        json_keys=['old_password','new_password']
        
        for key in json_keys:
            if key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_keys:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
            
        return {'status': True}
    except Exception as e:
       return {'data':e+"Internal Error",'status':False}


"""Admin profile update validator"""
def admin_profile_update_validator(data):#
    try:
        json_keys =['id','firstname','lastname','email','image','phone_number']
        json_values =['id','firstname','email','phone_number']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_values:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
            if val=='email':            
                result = functions.is_valid_email(data[val])
                if result == False:
                    return {'data':"please enter a valid email address",'status':False}
            if val=='phone_number':            
                result = functions.is_valid_phone(data[val])
                if result == False:
                    return {'data':"please enter a valid phonenumber",'status':False}
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}  

"""Employee profile create validator"""
def employee_create_validator(data):
    try:
        json_keys =['firstname','lastname','email','phone_number','employee_id','designation','roles']
        json_values =['firstname','lastname','email','phone_number','employee_id','designation','roles']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_values:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
            if val=='email':            
                result = functions.is_valid_email(data[val])
                if result == False:
                    return {'data':"please enter a valid email address",'status':False}
            if val=='phone_number':            
                result = functions.is_valid_phone(data[val])
                if result == False:
                    return {'data':"please enter a valid phonenumber",'status':False}
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}  

def employee_update_validator(data):
    try:
        json_keys =['firstname','lastname','phone_number','employee_id','designation','roles']
        json_values =['firstname','lastname','phone_number','employee_id','designation','roles']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_values:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
            if val=='email':            
                result = functions.is_valid_email(data[val])
                if result == False:
                    return {'data':"please enter a valid email address",'status':False}
            if val=='phone_number':            
                result = functions.is_valid_phone(data[val])
                if result == False:
                    return {'data':"please enter a valid phonenumber",'status':False}
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}  

def event_update_validator(data):
    try:
        json_keys =['event_title','description','choices','event_start','event_end','event_users']
        json_values =['event_title','description','choices','event_start','event_end','event_users']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_values:
            if type(data[val]) is str:
                if len(data[val]) == 0:
                    return {'data':val+" value is required",'status':False}
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}  