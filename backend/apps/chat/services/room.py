from apps.chat.constants import PERSONAL_CHANNEL_PREFIX
from apps.chat.models import RoomMember


def get_room_member_channels(room_id):
    """
    A helper method to return the list of channels for all current members of specific room.
    So that the change in the room may be broadcast to all the members.
    """
    members = RoomMember.objects.filter(room_id=room_id).values_list('user', flat=True)
    return [f'{PERSONAL_CHANNEL_PREFIX}:{user_id}' for user_id in members]
