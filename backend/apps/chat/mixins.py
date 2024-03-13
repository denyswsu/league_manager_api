from functools import partial

from django.db import transaction


from apps.chat.services import broadcast


class CentrifugoMixin:
    @staticmethod
    def broadcast_to_room(broadcast_payload):
        """
        Send a broadcast message to all members of the room.
        We need to use on_commit here to not send notification to Centrifugo before
        changes applied to the database. Since we are inside transaction.atomic block
        broadcast will happen only after successful transaction commit.
        """
        transaction.on_commit(partial(broadcast, broadcast_payload))
