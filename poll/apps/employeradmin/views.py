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
from apps.employee import models as employeemodel, serializers as employeeserializers
from apps.employeradmin import models as eventmodel, serializers as eventserializers


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


class Events(APIView):
    permission_classes=[permissions.IsAuthenticated,custom_permission.ISSuperAdmin]

    @csrf_exempt
    def post(self,request):
        try:
            datas = j.loads(request.body.decode('utf-8'))
            validation = validators.event_update_validator(datas)
           
            if validation['status']==False:
                return Json.Response({"data":[]},validation['data'], 400,False)
            
            employee_list = employeemodel.User.objects.filter(is_block=False).values_list("id",flat=True)
            
            if eventmodel.EventMaster.objects.filter(event_title=datas["event_title"]).exists():
                return Json.Response({"data":[]},"This event title had already been created", 400,False)
            
            if type(datas["event_users"]) is list:
                # check whether the given id is present in user table
                user_ids = set(employee_list)
                check_user = {}
                for users in datas["event_users"]:
                    check_user[users] = users in user_ids
                
                datas["event_users"]=[key for key, value in check_user.items() if value]
                datas["total_users"] = len(datas["event_users"])
            
            if datas["event_users"]=="all":
                datas["total_users"] = employeemodel.User.objects.filter(is_block=False).count()
                datas["event_users"] = list(employee_list)

            events = eventmodel.EventMaster.objects.create(**datas)
            
            for users in datas["event_users"]:
                user = employeemodel.User.objects.get(id=int(users))
                eventmodel.EventUserMapping.objects.create(event=events,event_user=user)
            
            choice_count = 0
            
            for choices in datas["choices"]:
                choice_count+=1
                eventmodel.EventChoiceMapping.objects.create(event=events,event_choice_name=choices,event_choice_id=choice_count)

            return Json.Response({"data":[datas]},"Event Created Successfully",200,True)
        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: While Creating event")
            return Json.Response({"data":[]},'Incorrect Details Please Check', 404,False)

    def get(self,request):
        try:
            if "id" not in request.query_params:
                return Json.Response({"data":[]},'key id not provided', 400,False)
            id=request.query_params.get('id')
            if id == "":
                return Json.Response({"data":[]},'Please provide user id', 400,False)
            event_obj = eventmodel.EventMaster.objects.filter(id=id)
            datas = eventserializers.EventSerializer(event_obj,many=True)
            return Json.Response({"data":[datas.data]},"Event viewed Successfully",200,True)
        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: While Viewing event")
            return Json.Response({"data":[]},'Incorrect Details Please Check', 404,False)

    def delete(self,request):
        try:
            if "id" not in request.query_params:
                return Json.Response({"data":[]},'key id not provided', 400,False)
            id=request.query_params.get('id')
            if id == "":
                return Json.Response({"data":[]},'Please provide user id', 400,False)
            if eventmodel.EventMaster.objects.filter(id=id,is_delete=True).exists():
                return Json.Response({"data":[]},'Event already deleted', 400,False)
            event_obj = eventmodel.EventMaster.objects.filter(id=id,is_delete=False).update(is_delete=True)
            return Json.Response({"data":[]},"Event Deleted Successfully",200,True)
        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: While Deleting event")
            return Json.Response({"data":[]},'Incorrect Details Please Check', 404,False)


class EventList(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]

    """
    Get the list of session slot list
    """
    queryset = eventmodel.EventMaster.objects.filter(is_delete = False).order_by('-created_on')
    serializer_class = eventserializers.EventSerializer
    
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
            
            logger.info(f"{current_date} {current_time} : Listing of events: Listed all Event Successfully")
            return data
        except Exception as e:
            logger.info(f"{current_date} {current_time} : {e}: Admin getting the list of Event")
            return Json.Response({"data":[]},'Internal Server Error', 404,False)