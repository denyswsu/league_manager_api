from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.chat.models import Room, Message, RoomMember

User = get_user_model()


class RoomSearchSerializer(serializers.ModelSerializer):
    is_member = serializers.BooleanField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'created_at', 'updated_at', 'is_member']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class LastMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'user', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    last_message = LastMessageSerializer(read_only=True)

    def get_member_count(self, obj):
        return obj.member_count

    class Meta:
        model = Room
        fields = ['id', 'name', 'version', 'member_count', 'last_message']


class MessageRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'version']


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = MessageRoomSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'user', 'room', 'created_at']


class RoomMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = RoomMember
        fields = ['room', 'user']
