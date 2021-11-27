from re import template
from typing import Awaitable
from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic.list import ListView
import pandas as pd


from datetime import date

from orders.models import *
from orders.ServicesOrders import *


class QueriesPanel(View):
    template_name = 'orders/queries/queries_panel.html'

    def get(self, request):
        return render(request, self.template_name)


class DynamicQueryView(ListView):
    model = Order
    template_name = 'orders/queries/query_dynamic.html'
    template_without_results = 'orders/queries/filter_form.html'

    def post(self, request, *args, **kwargs):
        to_search = {}
        if kwargs.get('date', None) != '0':
            to_search['date__gte'] = kwargs['date']
        if kwargs.get('id_order', None) != 0:
            to_search['id_order'] = kwargs['id_order']
        if kwargs.get('customer', None) != '0':
            to_search['customer__icontains'] = kwargs['customer']
        if kwargs.get('agent', None) != '0':
            to_search['agent__icontains'] = kwargs['agent']
        print(to_search)
        if len(to_search) > 0:
            orders = Order.objects.filter(**to_search)
        else:
            orders = Order.objects.all()
        if orders:
            page = request.GET.get('page', 1)
            paginator = Paginator(orders, 1)
            page_obj = paginator.page(page)
            orders = Order.objects.filter(id_order=page_obj.object_list[0].id_order)
            limit = range_for_paginations(paginator, page_obj, 5)

            products_order = ProductOrder.objects.filter(
                id_order_id__in=orders)
            values = ServicesReadPivot(
                orders.values(), products_order.values()).data()
            data = {
                'values': values,
                'paginator': paginator,
                'page_obj': page_obj,
                'limit': limit,
                'is_paginated': True
            }
            return render(request, self.template_name, data)
        else:
            messages.error(request, f'No se encontró información')
            return render(request, self.template_without_results)

    def get(self, request, **kwargs):
        return self.post(request, **kwargs)

class FilterView(View):
    template_name = 'orders/queries/filter_form.html'

    def get(self, request, **kwargs):
        data = {'next_page': ''}
        if kwargs['query'] == 'dynamic':
            data['next_page'] = 'order:dynamic_query'
        return render(request, self.template_name, data)
