from django.contrib import admin

# Register your models here.
from .models import RoomMember, Meeting, Attendance

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'creator', 'created_at')
    search_fields = ('room_name', 'creator__username')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'attendee', 'join_time', 'leave_time')
    list_filter = ('meeting', 'join_time')
    search_fields = ('attendee', 'meeting__room_name')

admin.site.register(RoomMember) 