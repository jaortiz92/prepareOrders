from django import forms
from orders.models import ProductOrder, Order


class ProductOrderFrom(forms.ModelForm):

    class Meta:
        model = ProductOrder
        fields = ('reference', 'color', 'size', 'quantity', 'price', 'total_price',
                  'line', 'brand', 'collection', 'cost', 'total_cost', 'status')
