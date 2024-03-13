from django.contrib import admin

from apps.chat.models import Room, RoomMember, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'created_at', 'bumped_at', 'last_message')
    search_fields = ('name',)


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'joined_at')
    list_filter = ('room', 'user')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'created_at')
    list_filter = ('room', 'user')
