from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone', 'location']
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category', 'size', 'image', 'created_at', 'owner', 'owner_email']
        read_only_fields = ['created_at', 'owner_email']
from .models import SwapRequest

class SwapRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapRequest
        fields = '__all__'
from .models import Chat, PracticeLog

class ChatSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'swap_request', 'sender', 'sender_username', 'message', 'timestamp']
        read_only_fields = ['sender', 'timestamp']


class PracticeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeLog
        fields = ['items_uploaded', 'swaps_made', 'last_active']
