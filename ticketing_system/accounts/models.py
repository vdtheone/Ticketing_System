from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    name = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    projects = models.ManyToManyField("Project", related_name="assigned_users")

    def __str__(self):
        return self.username


class Project(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Completed", "Completed"),
        ("Archived", "Archived"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
        ("Archived", "Archived"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    comment = models.TextField()

    def __str__(self):
        return self.name


class TicketAttachment(models.Model):
    TICKET_ATTACHMENT_CHOICES = [
        ("Image", "Image"),
        ("Video", "Video"),
        ("Docs", "Docs"),
    ]

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="attachments"
    )
    attachment = models.FileField(upload_to="ticket_attachments/")
    attachment_type = models.CharField(max_length=20, choices=TICKET_ATTACHMENT_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attachment_type} - {self.uploaded_at}"
