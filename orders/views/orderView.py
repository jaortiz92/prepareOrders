from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from orders.utils.utils import range_for_paginations
from django.urls import reverse_lazy

from django.contrib import messages
from datetime import datetime

from orders.models import *
from orders.ServicesOrders import *
from orders.forms import OrderFrom
# Create your views here.


class Panel(TemplateView):
    template_name = 'orders/panel.html'


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


class OrdersView(ListView):
    model = Order
    template_name = 'orders/orders.html'
    paginate_by = 10
    queryset = Order.objects.all()
    context_object_name = 'orders'

    def get_context_data(self, **kwargs: Any):
        contex = super().get_context_data(**kwargs)
        contex['limit'] = range_for_paginations(
            contex['paginator'], contex['page_obj'], 5)
        return contex


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
    template_error = 'orders/add_files_error.html'

    def get(self, request):
        data = ServicesAddNewOrders().data
        list_orders = []
        for row in data:
            if len(row['errors']['hard']) > 0:
                messages.error(request, 'Error al generar las ordenes')
                return render(request, self.template_error, {'data': data})
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
            'orders': list_orders,
            'data': data

        }

        return render(request, self.template_name, data)


class FilterForOrderView(View):
    template_name = 'orders/detail_order.html'

    def get(self, request, **kwars):
        query = ProductOrder.objects.filter(id_order_id=kwars['id_order'])
        order = Order.objects.get(id_order=kwars['id_order'])

        data = {
            'orders': [order],
            'products_order': query,
            'to_edit': False
        }
        return render(request, self.template_name, data)


class UpdateOrderView(UpdateView):
    template_name = 'orders/forms/update_order.html'
    form_class = OrderFrom
    queryset = Order.objects.all()
    pk_url_kwarg = 'id_order'
    success_url = reverse_lazy('order:orders')

    def post(self, request, *args, **kwargs):
        messages.success(
            request, f'Se modificó orden con ID {self.kwargs["id_order"]}')
        return super().post(request, *args, **kwargs)
