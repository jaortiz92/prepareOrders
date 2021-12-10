from django import forms
from orders.models import ProductOrder, Order


class ProductOrderFrom(forms.ModelForm):

    class Meta:
        model = ProductOrder
        fields = ('reference', 'color', 'size',  'line', 'brand',
                  'collection', 'quantity', 'price', 'total_price', 'cost', 'total_cost', 'status')


class OrderFrom(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('date', 'customer', 'file_name', 'agent', 'email')
