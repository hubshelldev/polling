"""
import django functions
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes,smart_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.hashers import make_password,check_password



"""
import restframeworks functions
"""
from rest_framework import generics, parsers, permissions, status
from rest_framework.views import APIView

"""
import apps,models,serializers
"""
from .models import *
from apps.employee import models, serializers


"""
import utils functions
"""
from utils.sendmail import send_custom_mail
from utils import validators
from utils import functions
from utils import json as Json
from utils import permissions as custom_permission
from utils.pagination import *

"""
Other Imports
"""
import json as j
import logging
logger = logging.getLogger( __name__ )
from datetime import datetime,timezone

"""
Swagger Imports
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
now = datetime.now(timezone.utc)
current_date = now.date()
current_time = now.time()

class Login(APIView):
    """
    Email and Password Login  API
    """
    permission_classes=[permissions.AllowAny]

    @csrf_exempt
    def post(self,request):
        
        try:
            datas = j.loads(request.body.decode('utf-8'))           

            """key validation""" 
            validation = validators.Email_login_validators(datas)
            if validation['status']==False:
                return Json.Response({"data":[]},validation['data'], 400,False)
            
            user_data = models.User.objects
            
            """checking the email exists in authUser or not """
            if not user_data.filter(email=datas['email']).exists():
                return Json.Response({"data":[]},"Please enter registered email",400, False)
            users = user_data.get(email=datas['email'])

                
            # if users.is_email_verified== False:
            #     return Json.Response({"data":[]},"Please verify the OTP before Login",400, False)
        
            if users.is_block==True:
                return Json.Response({"data":[]},"Admin blocked your account",400, False)

            if check_password(datas['password'],users.password) == False:
                return Json.Response({"data":[]},"Incorrect password",400, False)

            user_datas = user_data.get(email=datas['email'])
            user_obj=user_data.filter(email=datas['email'])
            user_Name_id =user_obj.first()
            
            user_details = {}

            """
            calling the access token function
            """

            getjwt=functions.emailauth(user_datas,user_Name_id.id)
            
            if getjwt == False:
                return Json.Response({"data":[]},"Error creating access token",400,False)

            user_details['access_token'] = getjwt['access_token']
            user_details['refresh_token'] = getjwt['refresh_token']
            user_details['user_info'] = {"id":user_Name_id.id,
                                                "name":str(user_Name_id.firstname)+' '+str(user_Name_id.lastname),
                                                "email":user_Name_id.email,
                                                "phone_number":user_Name_id.phone_number,
                                                "image":user_Name_id.image,
                                                "role_id":user_Name_id.roles_id}
            logger.info(f"{current_date} {current_time} : LoginAPi : Logged in Successfully")
            return Json.Response({"data":user_details},"Logged In Successfully",200,True)

        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: While login")
            return Json.Response({"data":[]},'Incorrect Login Details Please Check', 404,False)

class Employee(APIView):
    """
    Employee created by employer
    """
    permission_classes=[permissions.IsAuthenticated,custom_permission.ISSuperAdmin]
    serializers_class = serializers.EmployeeSerializer

    @csrf_exempt
    def post(self,request):
        try:
            datas =j.loads(request.body.decode('utf-8'))
            """
            Key validation
            """
            validation = validators.employee_create_validator(datas)
            if validation['status']==False:
                return Json.Response({"data":[]},validation['data'], 400,False)
            
            passwords = functions.generate_random_password()
            if not RoleMaster.objects.filter(id=datas["roles"]).exists():
                return Json.Response({"data":[]},"Role not present",400,False)
            
            datas["roles"]=RoleMaster.objects.get(id=datas["roles"])
            datas["password"]=make_password(str(passwords))
            
            if User.objects.filter(email=datas["email"]).exists():
                return Json.Response({"data":[]},"Email Already Exists",400,False)
            User.objects.create(**datas)
            logger.info(f"{current_date} {current_time} : Employee Create : User Created Successfully")
            return Json.Response({"data":[{"email":datas["email"],"password":str(passwords)}]},"User created Successfully",200,True)

        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: While Creating user")
            return Json.Response({"data":[]},'Incorrect Details Please Check', 404,False)
        
    def get(self,request):
        try:
            if "id" not in request.query_params:
                return Json.Response({"data":[]},'Please provide user id', 400,False)
            
            id=request.query_params.get('id')
            profile = User.objects.filter(id=id)
            if not profile.exists():
                return Json.Response({"data":[]},'Please provide valid user id', 400,False)
            
            result =serializers.EmployeeSerializer(profile, many=True).data
            logger.info(f"{current_date} {current_time} : Employee view: Viewed User Successfully")
            return Json.Response({"data":result},'Viewed User Successfully', 200,True)

        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: While viewing user")
            return Json.Response({"data":[]},'Error While viewing User', 404,False)
    
    def put(self,request):
        try:
            if "id" not in request.query_params:
                return Json.Response({"data":[]},'Please provide user id', 400,False)
            id=request.query_params.get('id')
            datas =j.loads(request.body.decode('utf-8'))
            validation = validators.employee_update_validator(datas)
           
            if validation['status']==False:
                return Json.Response({"data":[]},validation['data'], 400,False)

            if not RoleMaster.objects.filter(id=datas["roles"]).exists():
                return Json.Response({"data":[]},"Role not present",400,False)
            
            profile = User.objects.filter(id=id)
            if not profile.exists():
                return Json.Response({"data":[]},'Please provide valid user id', 400,False)
            
            profile.update(**datas)
            
            logger.info(f"{current_date} {current_time} : Employee Update : User Updated Successfully")
            return Json.Response({"data":[datas]},"User Updated Successfully",200,True)

        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: While updating user")
            return Json.Response({"data":[]},'Error While updating User', 404,False)

class EmployeeViewList(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]

    """
    Get the list of session slot list
    """
    queryset = User.objects.filter(is_block = False).order_by('-created_on')
    serializer_class = serializers.EmployeeSerializer
    
    def get(self, request):
        try:
            queryset = self.get_queryset()
            if (request.query_params.get('page') == None) or (request.query_params.get('page') == ""):
                pageno = 1
            else:
                pageno = request.query_params.get('page')
            
            if (request.query_params.get('limit') == None) or (request.query_params.get('limit') == ""):
                pagelimit = 10
            else:
                pagelimit = int(request.query_params.get('limit'))
            
            offset = 0
            page_cal = pagination_calculation(len(queryset),pagelimit)
            page_ = test_pagination(offset,pagelimit,pageno)
            
            result = queryset[page_[0]:page_[1]]
            if (request.query_params.get('page') and request.query_params.get('limit')):
                serializer = self.get_serializer(result, many=True)
                data = Json.Response({'total_count':page_cal[0],'total_page':page_cal[1],'page_per_limit':pagelimit,'data':serializer.data},'Listed successfully',200,True)
            else:
                serializer = self.get_serializer(result, many=True)
                data = Json.Response({'total_count':page_cal[0],'total_page':page_cal[1],'page_per_limit':pagelimit,'data':serializer.data},'data listed',200,True)
            
            logger.info(f"{current_date} {current_time} : Listing of employee: Listed all Employee Successfully")
            return data
        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: Admin getting the list of Employee")
            return Json.Response({"data":[]},'Internal Server Error', 404,False)