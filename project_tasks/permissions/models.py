from django.db import models
from core.models import Tenant 

class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True) 
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)  
    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f"{self.product.id}.{self.name}"

class Role(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('tenant', 'name')

    def __str__(self):
        return f"{self.tenant.name} - {self.name}"

class RoleFeaturePermission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('delete', 'Delete'),
    ]
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('role', 'feature', 'permission')

    def __str__(self):
        return f"{self.role.name} can {self.permission} on {self.feature}"