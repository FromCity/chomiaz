from rest_framework import serializers
from .models import Message


class MessageForUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    external_message_id = serializers.CharField()
    user_id = serializers.CharField()
    text = serializers.CharField()
    status = serializers.CharField()
    message_type = serializers.CharField()
    response_text = serializers.CharField()
    created_at = serializers.DateTimeField()
    processed_at = serializers.DateTimeField()

    class Meta:
        model = Message
        fields = ['id', 'external_message_id',
                  'user_id', 'text', 'status', 'message_type', 'response_text', 'created_at', 'processed_at']


class MessageDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    external_message_id = serializers.CharField()
    user_id = serializers.CharField()
    text = serializers.CharField()
    status = serializers.CharField()
    message_type = serializers.CharField()
    response_text = serializers.CharField()
    error_text = serializers.CharField()
    created_at = serializers.DateTimeField()
    received_at = serializers.DateTimeField()
    processed_at = serializers.DateTimeField()

    class Meta:
        model = Message
        fields = '__all__'
