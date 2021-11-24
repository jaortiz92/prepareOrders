from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import UpdateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy

from datetime import datetime

from django.views.generic.edit import DeleteView

from orders.models import *
from orders.ServicesOrders import *
from orders.forms import ProductOrderFrom


class ProductsOrderView(ListView):
    template_name = 'orders/orders_products.html'
    paginate_by  = 100
    queryset = ProductOrder.objects.all()
    context_object_name = 'products_order'
    def get_context_data(self, **kwargs: Any):
        contex = super().get_context_data(**kwargs)
        value_range = 5
        value_range_max = contex['paginator'].num_pages
        value_min = contex['page_obj'].number - value_range
        value_max = contex['page_obj'].number + value_range

        contex['limit'] = (value_min if value_max < value_range_max else value_range_max -  value_range * 2, value_max if value_min > 0 else value_range * 2)
        return contex

    

class UpdateProductOrderView(UpdateView):
    template_name = 'orders/update_product_order.html'
    form_class = ProductOrderFrom
    queryset = ProductOrder.objects.all()
    pk_url_kwarg = 'id_product_order'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy(
            'order:detail_order', kwargs={'id_order': self.object.id_order_id})
        messages.success(request, f'Se modificó producto con ID {self.object}')
        return super().post(request, *args, **kwargs)

class DeleteProductOrderView(View):
    model = ProductOrder

    def get(self, request, **kwars):
        id_product_order = kwars['id_product_order']
        id_product_order = ProductOrder.objects.get(id_product_order=id_product_order)
        id_product_order.delete()
        success_url = reverse_lazy(
            'order:detail_order', kwargs={'id_order': id_product_order.id_order_id})
        messages.success(
            request, f'Se eliminó producto {id_product_order}: {id_product_order.reference}')
        return redirect(success_url)