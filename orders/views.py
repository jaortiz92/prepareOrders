from django.shortcuts import render
from django.views import View
from orders.models import *
from datetime import datetime
# Create your views here.


class add_order(View):
    template_name = 'orders/add_order.html'

    def post(self, request):
        request.POST
        order = Order.objects.create(
            date=datetime.strptime(request.POST['date'], "%Y-%m-%d"),
            file_name=request.POST['file_name'],
            customer=request.POST['customer'],
            agent=request.POST['agent'],
        )
        return render(request, self.template_name, {'success': 'Datos agregados exitosamente'})

    def get(self, request):
        print(request)
        return render(request, self.template_name)
