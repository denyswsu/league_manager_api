from functools import partial

from apps.chat.serializers import BroadcastPayload
from apps.chat.services import broadcast
from django.db import transaction


class CentrifugoMixin:
    @staticmethod
    def broadcast_to_room(broadcast_payload: dict):
        """
        Validate broadcast payload and send a broadcast message to all members of the room.
        We need to use on_commit here to not send notification to Centrifugo before
        changes applied to the database. Since we are inside transaction.atomic block
        broadcast will happen only after successful transaction commit.
        """
        serializer = BroadcastPayload(data=broadcast_payload)
        serializer.is_valid(raise_exception=True)
        transaction.on_commit(partial(broadcast, serializer.validated_data))
