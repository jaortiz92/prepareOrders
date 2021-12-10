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
    path('orders/forms/update_product_order/<int:id_order>',
         views.UpdateOrderView.as_view(), name='update_order'),

    # Products Order
    path('products/', views.ProductsOrderView.as_view(), name='oders_products'),
    path('products/forms/update_product_order/<int:id_product_order>',
         views.UpdateProductOrderView.as_view(), name='update_product_order'),
    path('products/delete_product_order/<int:id_product_order>',
         views.DeleteProductOrderView.as_view(), name='delete_product_order'),
    # API Products Order
    path('products/update_product_order_api',
         views.update_product_order_view_API, name='update_product_order_api'),

    # Queries
    path('queries/', views.QueriesPanel.as_view(), name='queries_panel'),
    path('queries/filter/<str:query>/',
         views.FilterView.as_view(), name='queries_filter'),
    path('queries/dynamic/<str:date>/<int:id_order>/<str:customer>/<str:agent>',
         views.DynamicQueryView.as_view(), name='dynamic_query'),
    path('queries/dynamic_size/<str:date>/<int:id_order>/<str:customer>/<str:agent>',
         views.DynamicSizeQueryView.as_view(), name='dynamic_size'),
]
