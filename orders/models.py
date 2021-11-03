from django.db import models
# Create your models here.


class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    date = models.DateField()
    customer = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100, unique=True)
    agent = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['id_order']


class ProductOrder(models.Model):
    id_product_order = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reference = models.CharField(max_length=30, null=False)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=5)
    quantity = models.IntegerField(null=False)
    line = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    collection = models.CharField(max_length=40)
    status = models.CharField(max_length=150)
    price = models.FloatField()
    cost = models.FloatField()

    class Meta:
        db_table = 'products_order'
        verbose_name = 'ProductOrder'
        verbose_name_plural = 'ProductsOrder'
        ordering = ['id_product_order']
