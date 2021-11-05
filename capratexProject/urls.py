"""capratexProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from orders import views as orders_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/',  orders_views.panel.as_view(), name='panel_order'),
    path('orders/add_order/', orders_views.add_order.as_view(), name='add_order'),
    path('orders/products/', orders_views.oders_products.as_view(),
         name='oders_products'),
    path('orders/orders/', orders_views.orders.as_view(),
         name='orders'),
    path('orders/orders/detail_order/<int:id_order>', orders_views.filterForOrder.as_view(),
         name='orders'),
    path('orders/add_files/', orders_views.add_files.as_view(),
         name='add_files'),
    

]
