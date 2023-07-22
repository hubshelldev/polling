from cmath import exp
from hashlib import sha512
import json
import pytz
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import re
from apps.employeradmin import models as admin_models
from apps.employeradmin.models import *
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from random import randint
from base64 import b64encode

import string
import random
from apps.employee.models import *
from apps.employeradmin.models import *
from django.contrib.auth.hashers import make_password
from django.conf import settings
from utils.sendmail import send_custom_mail


#expiry time for verifing otp
def verifyexpiry_time(expirytime):
    try:
        utc = pytz.UTC
        curnt_time = datetime.now()
        dt_string = str(expirytime)
        new_dt = dt_string[:19]
        curnt_time = datetime.strptime(str(curnt_time), '%Y-%m-%d %H:%M:%S.%f')
        expire_ts = datetime.strptime(new_dt, '%Y-%m-%d %H:%M:%S')
        month_name = expirytime.strftime("%d")+" "+expirytime.strftime("%b") +" "+expirytime.strftime("%Y")
        time = expirytime.strftime("%H")+":"+expirytime.strftime("%M")
        curnt_time = curnt_time.replace(tzinfo=utc)
        expire_ts = expire_ts.replace(tzinfo=utc)
        return expire_ts,curnt_time
    except Exception as e:
        return False

def emailauth(user,id):
    try:
        access = AccessToken.for_user(user)
        refresh=RefreshToken.for_user(user)

        access['email']=user.email
        access['user_id']=id
        refresh['email']=user.email
        refresh['user_id']=id
        
        return {"access_token": str(access),
        "refresh_token":str(refresh)}
    except Exception as e:
        return False

def phoneauth(user,id):
    try:
        access = AccessToken.for_user(user)
        refresh=RefreshToken.for_user(user)

        access['email']=user.phone_number
        access['user_id']=id
        refresh['email']=user.phone_number
        refresh['user_id']=id
        
        return {"access_token": str(access),
        "refresh_token":str(refresh)}
    except Exception as e:
        return False

def is_valid_phone(phone):
    try:
        phone_number=re.compile(r'(^[+0-9]{1,3})*([0-9]{6,15}$)')
        data_phone=phone_number.match(phone)
        return True if data_phone != None else False
    except Exception as e:
        return None
    
def is_valid_email(email):
    try:
        email_validate=re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return True if re.fullmatch(email_validate, email) else False
    except Exception as e:
        return None
    
def is_valid_password1(password):
    try:
        password_validate=re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@()$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$')
        return True if  re.search(password_validate, password) else False
    except Exception as e:
        return False

def is_valid_password(password):
    try:
        password_validate=re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])(?=.*[\W_]).{8,}$')
        return True if  re.search(password_validate, password) else False
    except Exception as e:
        return False
    
def is_valid_latitude(latitude):
    pattern = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$'
    return True if re.match(pattern,latitude) else False
      

def is_valid_longitude(longitude):
    pattern = r'^[-+]?((1[0-7]|[1-9])?\d(\.\d+)?|180(\.0+)?)$'
    return True if re.match(pattern,longitude) else False

def is_valid_datetime(datetime):
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}$'
    return True if re.match(pattern,datetime) else False

def is_valid_date(date):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    value= date
    year= date[0:4]
    month=date[5:7]
    date = date[8:11]

    if re.match(pattern,value):
            if int(month) <=12:
                if int(date) <=31:
                    return True
                else:
                    return False
            else:
                return False
    else :
        return False

def is_valid_integer(value):
    try:
        value = int(value)
        return True
    except ValueError:
        return False
    

def year_valid(value):
    pattern = r'^\d{4}$'
    try:
        re.match(pattern,value)
        if int(value) <= datetime.now().year:
            return True
        else:
            return False
    except Exception as e:
        return False

def is_valid_url(url):
    https_pattern = r'^https:\/\/'
    http_pattern = r'^http:\/\/'
    try:
        if re.match(https_pattern, url) or re.match(http_pattern, url):
            return True
        else:
            return False
    except Exception as e:
        return False


# def event_polling_code():
#     try:
#         course_obj = RecreationalMaster.objects.latest('created_on')
#         count = 1
#         while count < 10:
#             recreational_code = course_obj.recreational_code[3:]
#             code = int(recreational_code) + count
#             code_format = '{:03}'.format(code)
#             course_code = "RCM" + str(code_format)
#             count += 1
#             if RecreationalMaster.objects.filter(recreational_code=course_code).count() == 0:
#                 break
#     except RecreationalMaster.DoesNotExist:
#         course_code = "RCM" + "001"
#     return course_code

def random_password():
    token_length = 9
    possible_characters = "abcdefghijklmnopqrstuvwxyz1234567890"
    print("-980")
    random_character_list = [random.choice(possible_characters) for i in range(token_length)]
    print()
    random_token = "".join(random_character_list)
    print(random_token)
    return random_token                


""" Language check validation function"""

def is_valid_integer(value):
    try:
        value = float(value)
        return True
    except ValueError:
        return False

def check_valid_format(string):
    try:
        date_object = datetime.strptime(string, '%Y-%m-%d')
        return True
    except Exception as e:
        return False

def age_calculation(dob):
    birthdate = dob
    date_of_birth=datetime.strptime(birthdate,"%Y-%m-%d")
    current_date = datetime.now()
    age = current_date.year -date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month,date_of_birth.day))
    return age

def generate_random_password():
    length = 8
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation.replace("_", "")  # Excluding underscore from special characters

    # Combine all characters without repetition
    all_chars = list(set(uppercase_letters + lowercase_letters + digits + special_characters))

    while True:
        # Ensure we have at least one character from each category
        password = (
            random.choice(uppercase_letters)
            + random.choice(lowercase_letters)
            + random.choice(digits)
            + random.choice(special_characters)
        )

        # Fill the rest of the password with random characters
        while len(password) < length:
            password += random.choice(all_chars)

        # Shuffle the password to ensure randomness
        password_list = list(password)
        random.shuffle(password_list)
        password = ''.join(password_list)

        # Check if the password satisfies the regex
        if re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])(?=.*[\W_]).{8,}$', password):
            return password

# Generate a random password
# random_password = generate_random_password()
# print(random_password)

