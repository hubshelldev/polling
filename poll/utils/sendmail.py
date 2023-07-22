"""
Django imports
"""
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,send_mail
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.contrib.staticfiles import finders

"""
Other Imports
"""
from poll import settings
from datetime import datetime, timedelta
import pytz,random
from decouple import config as cnf
import logging
from io import BytesIO
import os

"""
Import apps and models
"""
from apps.employee.models import *
"""
Logger initialization
"""
logger = logging.getLogger( __name__ )

# from twilio.rest import Client

def send_custom_mail(message, recepiants, subject,template):
    
    """
    Sending Custom mail fucntion which is callable
    """
    
    try:
        email_html_message = render_to_string(template, message)
        email = EmailMultiAlternatives(subject, email_html_message, settings.DEFAULT_FROM_EMAIL, [recepiants])
        email.attach_alternative(email_html_message, "text/html")
        email.send()
    except Exception as e:
        logger.info(f"{e} :send mail")
        pass

def send_SMS(numbers,message):

    """
    Sending custom SMS function which is callable
    """
    
    try:
        # client = Client(cnf('TWILIO_ACCOUNT_SID'), cnf('TWILIO_AUTH_TOKEN') )
        # client.messages.create(to=numbers,from_=cnf('TWILIO_NUMBER'),body=message)
        # data = urllib.parse.urlencode(
        #     {'apikey': settings.TEXT_LOCAL_API_KEY, 'numbers': numbers, 'message': message, 'sender': sender})
        # data = data.encode('utf-8')
        # request = urllib.request.Request("https://api.textlocal.in/send/?")
        # f = urllib.request.urlopen(request, data)
        # fr = f.read()
        return True
    except:
        pass


def temp_email_otp(email,subject,template):
    
    """
    Sending temporary OTP to email which is callable
    """
    
    try:
        otp_val=random.randint(1000,9999)

        # "dummy otp val static purpose"
        # otp_val = 1212
        # print(otp_val,'----------')

        expire_ts=datetime.now()+timedelta(minutes=2)

        context = {
            'email': email,
            'otp': otp_val,
        }
        
        if not TempOTP.objects.filter(email=email).exists():
                otptbl = TempOTP(otp = otp_val,expired_by = expire_ts,email=email)
                otptbl.save()
        else:
            TempOTP.objects.filter(email=email).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())
        
        send_custom_mail(context, email, subject,template)
        id = TempOTP.objects.filter(email=email).first().id
        return id

    except Exception as e:
        return False

def temp_mobile_otp(phone_number):
    
    """
    Sending temporary OTP to phonenumber which is callable
    """

    try:
        otp_val=random.randint(1000,9999)
        
        "dummy otp val static purpose"
        # otp_val = 1212
        
        message = F"temperory otp for registeration:{otp_val}"
        expire_ts=datetime.now()+timedelta(minutes=2)
        
        if not TempOTP.objects.filter(phone=phone_number).exists():
                otptbl = TempOTP(otp = otp_val,expired_by = expire_ts,phone=phone_number)
                otptbl.save()
        else:
            TempOTP.objects.filter(phone=phone_number).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())
        
        id = TempOTP.objects.filter(phone=phone_number).first().id
        ph_number = str(phone_number)

        '''send otp to client TextLocal Credentials'''

        # send_SMS(ph_number,message)

        return id,otp_val
        
    except Exception as e:
        return False


def send_mobile_otp(phone_number,country_code,id):
    otp_val=random.randint(1000,9999)
    # "dummy otp val static purpose"
    # otp_val = 1212
    message = F"Hi there,your verification code is:{otp_val}"
    
    expire_ts=datetime.now()+timedelta(minutes=2)
    if not OTPAuth.objects.filter(user_id=id).exists():
            otptbl = OTPAuth(otp = otp_val,expired_by = expire_ts,user_id=id)
            otptbl.save()
    else:
        OTPAuth.objects.filter(user_id=id).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())
    ph_number = str(phone_number)

    '''send otp to client TextLocal Credentials'''
    send_SMS(ph_number,message)

    return otp_val

def send_email_otp(email,id,subject,template):
    otp_val=random.randint(1000,9999)
    # "dummy otp val static purpose"
    # otp_val = 1212
    expire_ts=datetime.now()+timedelta(minutes=2)
    

    context = {
        'email': email,
        'otp': otp_val,
    }
    if not OTPAuth.objects.filter(user_id=id).exists():
            otptbl = OTPAuth(otp = otp_val,expired_by = expire_ts,user_id=id)
            otptbl.save()
    else:
        OTPAuth.objects.filter(user_id=id).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())

    send_custom_mail(context, email, subject,template)
    return otp_val