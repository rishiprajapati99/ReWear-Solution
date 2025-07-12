from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    points = models.PositiveIntegerField(default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.email



class Item(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default='Clothing')  
    size = models.CharField(max_length=20)
    condition = models.CharField(max_length=50, default='Good')  
    tags = models.CharField(max_length=200, blank=True)
    available = models.BooleanField(default=True)  
    image = models.ImageField(upload_to='item_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.owner.email}"



class SwapRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    item_from = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='swap_requests_made'
    )
    item_to = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='swap_requests_received'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_from} ⇄ {self.item_to} [{self.status}]"


class PracticeLog(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='practice_log'
    )
    items_uploaded = models.PositiveIntegerField(default=0)
    swaps_made = models.PositiveIntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Uploads: {self.items_uploaded}, Swaps: {self.swaps_made}"


class Chat(models.Model):
    swap_request = models.ForeignKey(SwapRequest, on_delete=models.CASCADE, related_name='chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.swap_request.status != 'approved':
            raise ValidationError("Chat is only allowed for approved swaps.")

    def __str__(self):
        return f"Chat from {self.sender.username} on swap #{self.swap_request.id}"

