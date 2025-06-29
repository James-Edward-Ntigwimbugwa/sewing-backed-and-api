from django.db import models
from django.forms import ValidationError
from users.models import CustomUser

# Create your models here.
class ProductDetail(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    suk = models.CharField(max_length=100)  # Removed duplicate field

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='products')
        
    def clean(self):
        if self.cost < 0:
             raise ValidationError('Cost cannot be negative.')

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name