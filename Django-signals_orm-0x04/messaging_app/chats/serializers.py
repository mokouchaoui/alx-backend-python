from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role_description = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'role_description', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
