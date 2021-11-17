from django.urls import path
from orders import views

urlpatterns = [
    path('',  views.Panel.as_view(), name='panel'),

    # Orders
    path('add_order/', views.AddOrderView.as_view(), name='add_order'),

    path('orders/', views.OrdersView.as_view(),
         name='orders'),
    path('orders/detail_order/<int:id_order>', views.FilterForOrderView.as_view(),
         name='detail_order'),
    path('orders/delete_order/<int:id_order>', views.DeleteOrderView.as_view(),
         name='delete_order'),
    path('add_files/', views.AddFilesView.as_view(),
         name='add_files'),

    # Products Order
    path('products/', views.ProductsOrderView.as_view(), name='oders_products'),
    path('products/update_product_order/<int:id_product_order>',
         views.UpdateProductOrderView.as_view(), name='update_product_order'),

    # Queries
    path('queries/', views.QueriesPanel.as_view(), name='queries_panel'),
    path('queries/filter', views.FilterView.as_view(), name='queries_filter'),
    path('queries/dynamic/', views.DynamicQueryView.as_view(), name='dynamic_query'),
]
