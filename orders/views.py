from re import template
import typing
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from orders.models import *
from datetime import datetime
import json
from orders.ServicesOrders import *
# Create your views here.


class panel(View):
    template_name = 'orders/panel.html'

    def get(self, request):
        return render(request, self.template_name)


class add_order(View):
    template_name = 'orders/add_order.html'

    def post(self, request):
        request.POST
        order = Order.objects.create(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            file_name=request.POST['file_name'],
            customer=request.POST['customer'],
            agent=request.POST['agent'],
        )
        return render(request, self.template_name, {'success': 'Datos agregados exitosamente'})

    def get(self, request):
        print(request)
        return render(request, self.template_name)


class oders_products(ListView):
    model = ProductOrder
    template_name = 'orders/orders_products.html'


class orders(ListView):
    model = Order
    template_name = 'orders/orders.html'


class add_files(View):

    template_name = 'orders/add_files.html'

    def get(self, request):
        data = ServicesAddNewOrders().data
        list_orders = []

        for order in data:
            order_created = Order.objects.create(**order['order'])
            list_orders.append(order_created)
            list_order_product = []
            for order_product in order['productsOrder']:
                product_order = ProductOrder(
                    **order_product, id_order=order_created)
                list_order_product.append(product_order)
            ProductOrder.objects.bulk_create(list_order_product)

        data = {
            'orders': list_orders
        }

        return render(request, self.template_name, data)
