from django.db import transaction
from django.db.models import OuterRef, Exists, Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.chat.constants import USER_LEFT, USER_JOINED, MESSAGE_ADDED
from apps.chat.mixins import CentrifugoMixin
from apps.chat.models import RoomMember, Room, Message
from apps.chat.serializers import (
    RoomSearchSerializer, RoomSerializer, MessageSerializer, RoomMemberSerializer,
)
from apps.chat.services import get_room_member_channels


class RoomSearchViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_membership = RoomMember.objects.filter(
            room=OuterRef('pk'),
            user=user
        )
        return Room.objects.annotate(
            is_member=Exists(user_membership)
        ).order_by('name')


class RoomListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.annotate(
            member_count=Count('memberships')
        ).filter(
            memberships__user_id=self.request.user.pk
        ).prefetch_related(
            'last_message', 'last_message__user'
        ).order_by('-memberships__joined_at')
        return queryset


class RoomDetailViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.annotate(
            member_count=Count('memberships')
        ).filter(memberships__user_id=self.request.user.pk)


class MessageListCreateAPIView(ListCreateAPIView, CentrifugoMixin):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        get_object_or_404(RoomMember, user=self.request.user, room_id=room_id)
        return Message.objects.filter(room_id=room_id).prefetch_related(
            'user', 'room'
        ).order_by('-created_at')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # TODO: move out all the logic to a service
        room_id = self.kwargs['room_id']
        room = Room.objects.select_for_update().get(id=room_id)
        room.increment_version()
        channels = get_room_member_channels(room_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(room=room, user=request.user)
        room.last_message = obj
        room.save()

        # This is where we add code to broadcast over Centrifugo API.
        broadcast_payload = {
            'channels': channels,
            'data': {
                'type': MESSAGE_ADDED,
                'body': serializer.data
            },
            'idempotency_key': f'{MESSAGE_ADDED}_{serializer.data["id"]}'
        }
        self.broadcast_to_room(broadcast_payload)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class JoinRoomView(APIView, CentrifugoMixin):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, room_id):
        # TODO: move out all the logic to a service
        room = Room.objects.select_for_update().get(id=room_id)
        room.increment_version()
        if RoomMember.objects.filter(user=request.user, room=room).exists():
            return Response({"message": "already a member"}, status=status.HTTP_409_CONFLICT)

        obj, _ = RoomMember.objects.get_or_create(user=request.user, room=room)
        channels = get_room_member_channels(room_id)
        obj.room.member_count = len(channels)
        body = RoomMemberSerializer(obj).data

        broadcast_payload = {
            'channels': channels,
            'data': {
                'type': USER_JOINED,
                'body': body
            },
            'idempotency_key': f'{USER_JOINED}_{obj.pk}'
        }
        self.broadcast_to_room(broadcast_payload)
        return Response(body, status=status.HTTP_200_OK)


class LeaveRoomView(APIView, CentrifugoMixin):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, room_id):
        # TODO: move out all the logic to a service
        room = Room.objects.select_for_update().get(id=room_id)
        room.increment_version()
        channels = get_room_member_channels(room_id)
        obj = get_object_or_404(RoomMember, user=request.user, room=room)
        obj.room.member_count = len(channels) - 1
        pk = obj.pk
        obj.delete()
        body = RoomMemberSerializer(obj).data

        broadcast_payload = {
            'channels': channels,
            'data': {
                'type': USER_LEFT,
                'body': body
            },
            'idempotency_key': f'{USER_LEFT}_{pk}'
        }
        self.broadcast_to_room(broadcast_payload)
        return Response(body, status=status.HTTP_200_OK)
