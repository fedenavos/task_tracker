from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    is_urgent = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'estimate', 'state', 'is_urgent']

    def validate_estimate(self, value):
        if value < 0:
            raise serializers.ValidationError("The estimate can't be negative")
        return value
    
    def validate_state(self, value):
        valid_states = [choice[0] for choice in Task.STATE_CHOICES]
        if value not in valid_states:
            raise serializers.ValidationError("The state is not valid")
        return value
    
    def get_is_urgent(self, obj):
        return obj.estimate < 4
