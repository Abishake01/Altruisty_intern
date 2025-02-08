from django.db import models
import uuid
from datetime import datetime

class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    ]

    LEVEL_CHOICES = [
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
    ]

    ticket_id = models.BigIntegerField(unique=True)  # 12-digit unique number
    login_id = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)  # Automatically sets date when created
    created_time = models.TimeField(auto_now_add=True)  # Automatically sets time when created
    closed_date = models.DateField(null=True, blank=True)  # Can be null
    closed_time = models.TimeField(null=True, blank=True)  # Can be null
    title = models.CharField(max_length=250)
    issue_type = models.CharField(
        max_length=20,
        choices=[
            ('Technical', 'Technical'),
            ('Payment', 'Payment'),
            ('Others', 'Others'),
        ],
    )
    description = models.TextField()
    attachment = models.BinaryField(null=True, blank=True)  # Binary field for storing files
    assigned_to = models.JSONField(null=True, blank=True)  # JSON field for assigned_to
    company_name = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='Pending')
    levels = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True)  # Levels as integers
    attribute1 = models.TextField(null=True, blank=True)
    attribute2 = models.TextField(null=True, blank=True)
    attribute3 = models.TextField(null=True, blank=True)
    attribute4 = models.TextField(null=True, blank=True)
    attribute5 = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            # Generate a random 12-digit number for ticket_id
            self.ticket_id = uuid.uuid4().int >> 116  # Generate a random large number and take first 12 digits
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket #{self.ticket_id} - {self.title}"

    class Meta:
        db_table = 'tickets'
