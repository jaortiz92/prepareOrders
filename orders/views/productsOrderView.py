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
from orders.utils.utils import range_for_paginations

class ProductsOrderView(ListView):
    template_name = 'orders/orders_products.html'
    paginate_by = 100
    queryset = ProductOrder.objects.all()
    context_object_name = 'products_order'
    def get_context_data(self, **kwargs: Any):
        contex = super().get_context_data(**kwargs)
        contex['limit'] = range_for_paginations(contex['paginator'], contex['page_obj'], 5)
        return contex

    

class UpdateProductOrderView(UpdateView):
    template_name = 'orders/forms/update_product_order.html'
    form_class = ProductOrderFrom
    queryset = ProductOrder.objects.all()
    pk_url_kwarg = 'id_product_order'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy(
            'order:detail_order', kwargs={'id_order': self.object.id_order_id})

        form = self.get_form()
        if form.is_valid():
            messages.success(request, f'Se modificó producto con ID {self.kwargs["id_product_order"]}')
            
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