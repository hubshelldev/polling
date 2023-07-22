from rest_framework import serializers
from apps.employeradmin.models import *

class choiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventChoiceMapping
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    choices =serializers.SerializerMethodField('get_choice')
    def get_choice(self, data):
        choice = EventChoiceMapping.objects.filter(event_id=data.id)
        roles = choiceSerializer(choice,many=True).data
        return roles
    
    class Meta:
        model = EventMaster
        fields = "__all__"
