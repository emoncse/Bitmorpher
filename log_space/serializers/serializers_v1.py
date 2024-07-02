from rest_framework import serializers

from log_space.models import APILog


class LogSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = APILog
        fields = ['username', 'date_time']
        extra_kwargs = {'date_time': {'read_only': True}}