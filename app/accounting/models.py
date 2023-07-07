from django.db import models
from sales.models import Sale


# Create your models here.

class Bills(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Profit(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)