from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

from datetime import datetime

from orders.models import *
from orders.ServicesOrders import *
# Create your views here.


class Panel(View):
    template_name = 'orders/panel.html'

    def get(self, request):
        return render(request, self.template_name)


class AddOrderView(View):
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


class ProductsOrderView(View):
    template_name = 'orders/orders_products.html'

    def get(self, request):
        query = ProductOrder.objects.all()
        data = {
            'products_order': query
        }

        return render(request, self.template_name, data)


class OrdersView(View):
    model = Order
    template_name = 'orders/orders.html'

    def get(self, request):
        query = Order.objects.all()
        data = {
            'orders': query,
            'to_edit': True
        }
        return render(request, self.template_name, data)


class DeleteOrderView(View):
    model = Order
    template_name = 'orders'

    def get(self, request, **kwars):
        id_order = kwars['id_order']
        order = Order.objects.get(id_order=id_order)
        order.delete()
        messages.success(
            request, f'Se eliminó orden {id_order} del archivo {order.file_name}')
        return redirect(to='order:orders')


class AddFilesView(View):

    template_name = 'orders/add_files.html'

    def get(self, request):
        data = ServicesAddNewOrders().data
        list_orders = []
        counter = 0

        for order in data:
            order_created = Order.objects.create(**order['order'])
            list_orders.append(order_created)
            list_order_product = []
            for order_product in order['productsOrder']:
                product_order = ProductOrder(
                    **order_product, id_order=order_created)
                list_order_product.append(product_order)
            ProductOrder.objects.bulk_create(list_order_product)
            counter += 1
        messages.success(request, f'Se agregaron {counter} archivos')
        data = {
            'orders': list_orders
        }

        return render(request, self.template_name, data)


class FilterForOrderView(View):
    template_name = 'orders/detail_order.html'

    def get(self, request, **kwars):
        query = ProductOrder.objects.filter(id_order_id=kwars['id_order'])
        order = Order.objects.get(id_order=kwars['id_order'])

        data = {
            'orders': [order],
            'products_order': query
        }
        return render(request, self.template_name, data)
