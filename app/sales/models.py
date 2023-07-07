from datetime import date, datetime, time, timezone

from django.db import models
from django.db.models import Count, F, Sum
from inventory.models import Product
from users.models import Client

# Create your models here.


class Sale(models.Model):
    ORDER = 'ORDER'
    COMPLETED = 'COMPLETE'
    CANCELED = 'CANCELED'

    STATUS_SALE_CHOICES = (
        ('ORDER', 'Pedido'),
        ('COMPLETED', 'Venta completada'),
        ('CANCELED', 'Cancelada'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    status = models.CharField('Estado', max_length=20,
                              choices=STATUS_SALE_CHOICES)
    created_at = models.DateTimeField('Fecha venta', auto_now_add=True)
    updated_at = models.DateTimeField(
        'Fecha modificacion venta', auto_now=True)

    def get_products(self):
        return self.products.all()

    def calculate_total_price(self):
        total_price = self.products.aggregate(total=Sum('price')).get('total')
        return total_price if total_price else 0

    def calculate_total_quantity(self):
        total_quantity = self.products.aggregate(
            total=Sum('quantity')).get('total')
        return total_quantity if total_quantity else 0

    @classmethod
    def get_completed_sales_total_day(cls):
        today = timezone.now().date()
        start_datetime = datetime.combine(today, time())

        completed_sales = cls.objects.filter(
            status='COMPLETED',
            created_at__range=(start_datetime, timezone.now())
        ).annotate(num_sales=Count('id'))

        return completed_sales.count()

    @classmethod
    def get_completed_sales_day(cls):
        today = date.today()
        start_datetime = datetime.combine(today, time())
        completed_sales = cls.objects.filter(
            status='COMPLETED', created_at__gte=start_datetime)
        total_sales = completed_sales.annotate(total_price=Sum(F('products__price'))) \
            .aggregate(total=Sum('total_price')) \
            .get('total')
        return total_sales if total_sales else 0

    @classmethod
    def get_completed_sales_month(cls):
        today = date.today()
        start_of_month = today.replace(day=1)
        start_datetime = datetime.combine(start_of_month, time())

        completed_sales = cls.objects.filter(
            status='COMPLETED',
            created_at__gte=start_datetime,
            created_at__lt=datetime.now()
        )

        total_sales = completed_sales.aggregate(
            total_price=Sum(F('products__price')))['total_price']

        return total_sales if total_sales else 0

    def __str__(self):
        return f"Venta {self.client} {self.created_at}"
