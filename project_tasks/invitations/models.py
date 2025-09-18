from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone

class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
        ('canceled', 'Canceled'),
    ]

    name = models.CharField(max_length=100)  
    email = models.EmailField()
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    token = models.CharField(max_length=50, unique=True)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True) 
    note = models.TextField(blank=True)  

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(50)  
        if not self.expiration_date:
            self.expiration_date = timezone.now() + timezone.timedelta(days=7)  # Set 7 days later
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invitation for {self.email} to {self.tenant.name}"

    def is_expired(self):
        return timezone.now() > self.expiration_date