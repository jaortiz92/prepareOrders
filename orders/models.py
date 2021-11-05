from django.db import models
from datetime import datetime
# Create your models here.


class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    date = models.DateTimeField()
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

    def row(self):
        print(self.date)
        row = {
            'id_order': self.id_order,
            'date': self.date.strftime('%Y-%m-%d'),
            'customer': self.customer,
            'agent': self.agent,
            'file_name': self.file_name,
            'created': self.created.strftime('%Y-%m-%d, %H:%M:%S'),
            'modified': self.modified.strftime('%Y-%m-%d, %H:%M:%S')
        }
        return row

    def __str__(self) -> str:
        return str(self.id_order)


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
    total_price = models.FloatField()
    cost = models.FloatField()
    total_cost = models.FloatField()

    def row(self):
        row = {
            'id_product_order': self.id_product_order,
            'id_order_id': self.id_order_id,
            'reference': self.reference,
            'color': self.color,
            'size': self.size,
            'quantity': self.quantity,
            'price': self.price,
            'total_price': self.total_price,
            'line': self.line,
            'brand': self.brand,
            'collection': self.collection,
            'cost': self.cost,
            'total_cost': self.total_cost,
            'status': self.status
        }
        return row

    def __str__(self) -> str:
        return str(self.reference)

    class Meta:
        db_table = 'products_order'
        verbose_name = 'ProductOrder'
        verbose_name_plural = 'ProductsOrder'
        ordering = ['id_product_order']
