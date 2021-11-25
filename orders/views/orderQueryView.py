from re import template
from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
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
    template_name = 'orders/queries/query_dynamic.html'
    template_name_filter = 'orders/queries/filter_form.html'

    def post(self, request, **kwargs):
        to_search = {}
        if request.POST['date']:
            to_search['date__gte'] = request.POST['date']
        if request.POST['id_order']:
            to_search['id_order'] = request.POST['id_order']
        if request.POST['customer']:
            to_search['customer__icontains'] = request.POST['customer']
        if request.POST['agent']:
            to_search['agent__icontains'] = request.POST['agent']

        if len(to_search) > 0:
            orders = Order.objects.filter(**to_search)
        else:
            orders = Order.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(orders, 1)
        page_obj = paginator.page(page)
        orders = Order.objects.filter(id_order=page_obj.object_list[0].id_order)
        limit = range_for_paginations(paginator, page_obj, 5)
        if orders:
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
            return render(request, self.template_name_filter)


class FilterView(View):
    template_name = 'orders/queries/filter_form.html'
    template_name_sub = 'orders/queries/query_dynamic.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        view = DynamicQueryView()
        return view.post(request, **kwargs)
