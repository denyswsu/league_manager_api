from apps.chat.constants import ALL_MESSAGE_TYPES
from apps.chat.models import Message, Room, RoomMember
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class LastMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "content", "user", "created_at"]


class RoomSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    last_message = LastMessageSerializer(read_only=True)

    def get_member_count(self, obj):
        return obj.member_count

    class Meta:
        model = Room
        fields = ["id", "name", "version", "member_count", "last_message", "bumped_at"]


class RoomSearchSerializer(serializers.ModelSerializer):
    is_member = serializers.BooleanField(read_only=True)

    class Meta:
        model = Room
        fields = ["id", "name", "created_at", "bumped_at", "is_member"]


class MessageRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "version", "bumped_at"]


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = MessageRoomSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "content", "user", "room", "created_at"]


class RoomMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = RoomMember
        fields = ["room", "user"]


class BroadcastData(serializers.Serializer):
    type = serializers.ChoiceField(choices=ALL_MESSAGE_TYPES)
    body = serializers.DictField()


class BroadcastPayload(serializers.Serializer):
    """
    data = {
        'channels': channels,  # A list of channels to broadcast the message to.
        'data': {
            'type': 'user_left',  # The type of the message.
            'body': body  # The data to be broadcast.
        },
        'idempotency_key': f'user_left_{pk}'  # A unique key to prevent duplicate messages.
    }
    """

    channels = serializers.ListField(child=serializers.CharField())
    idempotency_key = serializers.CharField()
    data = BroadcastData()
