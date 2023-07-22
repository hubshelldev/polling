from rest_framework import serializers
from apps.employee.models import *

class EmployeeSerializer(serializers.ModelSerializer):
    role_name =serializers.SerializerMethodField('get_role')
    def get_role(self, data):
        roles = RoleMaster.objects.get(id=data.roles_id).name
        return roles
    
    class Meta:
        model = User
        fields = ('id','firstname','lastname','email','phone_number','roles','is_block','employee_id','designation','role_name')
