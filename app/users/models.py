from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):

    TYPE_CHOICES = (
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
        ('staff', 'Personal'),
    )

    user_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField('Direccion', max_length=255, blank=True)
    phone_number = models.CharField('Celular', max_length=20)
    date_of_birth = models.DateField('Fecha de nacimiento', blank=True, null=True)


    def get_full_name(self):
        return self.user.get_full_name()

    def get_username(self):
        return self.user.username


    @classmethod
    def create_with_phone_number(cls, phone_number):
        user = CustomUser.objects.create(username=phone_number)
        cliente = cls.objects.create(user=user, phone_number=phone_number)
        return cliente

    
    def get_sales(self):
        from sales.models import Sale  # Para evitar importación circular
        return Sale.objects.filter(client=self).order_by('-created_at')


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Agrega tus campos adicionales para el modelo Admin aquí

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Agrega tus campos adicionales para el modelo Staff aquí
