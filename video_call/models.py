from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RoomMember(models.Model):  
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Meeting(models.Model):
    room_name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings')
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)  # Ensure this field is added

    def __str__(self):
        return f"{self.room_name} - {self.created_at.date()}"

class Attendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    attendee = models.CharField(max_length=200)
    join_time = models.DateTimeField()  # Changed from auto_now_add
    leave_time = models.DateTimeField(null=True, blank=True)
    attendance_percentage = models.FloatField(default=0)
    is_present = models.BooleanField(default=False)
    
    def calculate_attendance_percentage(self):
        if self.leave_time and self.join_time and self.meeting.duration:
            attendance_duration = self.leave_time - self.join_time
            percentage = (attendance_duration.total_seconds() / self.meeting.duration.total_seconds()) * 100
            self.attendance_percentage = min(percentage, 100)
            self.is_present = self.attendance_percentage >= 75
            self.save()
            print(f"Calculated attendance for {self.attendee}: {self.attendance_percentage}%")
        else:
            print(f"Missing data for calculating attendance for {self.attendee}")

    def __str__(self):
        return f"{self.attendee} - {self.meeting.room_name} ({self.attendance_percentage:.1f}%)"

    class Meta:
        ordering = ['-join_time']
