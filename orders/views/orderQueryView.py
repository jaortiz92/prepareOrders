from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic.list import ListView

from orders.models import *
from orders.ServicesOrders import *
from orders.utils import select_to_search_order


class QueriesPanel(View):
    template_name = 'orders/queries/queries_panel.html'

    def get(self, request):
        return render(request, self.template_name)


class DynamicQueryView(ListView):
    model = Order
    template_name = 'orders/queries/query_dynamic.html'
    template_without_results = 'orders/queries/filter_form.html'

    def post(self, request, *args, **kwargs):
        to_search = select_to_search_order(kwargs)

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
            return render(request, self.template_without_results, {'next_page': 'dynamic'})

    def get(self, request, **kwargs):
        return self.post(request, **kwargs)


class DynamicSizeQueryView(View):
    template_name = 'orders/queries/query_dynamic_size.html'
    template_without_results = 'orders/queries/filter_form.html'
    
    def get(self, request, **kwargs):
        to_search = select_to_search_order(kwargs)
        if len(to_search) > 0:
            orders = Order.objects.filter(**to_search)
        else:
            orders = Order.objects.all()

        if orders:
            products_order = ProductOrder.objects.filter(id_order_id__in=orders)
            values = ServicesReadPivotSize(products_order.values()).data()
            data = {
                'values': values,
            }
            return render(request, self.template_name, data)
        else:
            messages.error(request, f'No se encontró información')
            return render(request, self.template_without_results, {'next_page': 'dynamic_size'})


class FilterView(View):
    template_name = 'orders/queries/filter_form.html'

    def get(self, request, **kwargs):
        data = {'next_page': ''}
        if kwargs['query'] == 'dynamic':
            data['next_page'] = 'dynamic'
        elif kwargs['query'] == 'dynamic_size':
            data['next_page'] = 'dynamic_size'
        return render(request, self.template_name, data)
