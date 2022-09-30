from django.db import models

# Create your models here.
class Table(models.Model):
    number = models.AutoField(primary_key=True)
    order_number = models.IntegerField("Номер заказа", default=False)
    price_usd = models.IntegerField("Цена, $", default=False)
    price_rub = models.IntegerField("Цена, руб", default=False)
    delivery_time = models.CharField("Срок поставки", max_length=100)
