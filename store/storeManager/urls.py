from django.urls import path
from . import views

urlpatterns = [
    # Home URLs
    path('', views.home, name='home'),
    
    # Market URLs
    path('markets/', views.MarketListView.as_view(), name='market_list'),
    path('markets/add/', views.MarketCreateView.as_view(), name='market_add'),
    path('markets/<int:pk>/edit/', views.MarketUpdateView.as_view(), name='market_edit'),
    path('markets/<int:pk>/delete/', views.MarketDeleteView.as_view(), name='market_delete'),
    path('markets/<int:pk>/addsalesman', views.SalesmanCreateView.as_view(), name='market_addsalesman'),
    path('markets/<int:pk>/addcustomer', views.CustomerCreateView.as_view(), name='market_addcustomer'),
    
     # Salesman URLs
    path('salesman/', views.SalesmanListView.as_view(), name='salesman_list'),
    path('salesman/add', views.SalesmanCreateView.as_view(), name='salesman_add'),
    path('salesman/<int:pk>/edit/', views.SalesmanUpdateView.as_view(), name='salesman_edit'),
    path('salesman/<int:pk>/delete/', views.SalesmanDeleteView.as_view(), name='salesman_delete'),
    path('salesman/<int:pk>/addproduct', views.ProductCreateView.as_view(), name='salesman_addproduct'),
    path('salesman/<int:pk>/addorder', views.OrderCreateView.as_view(), name='salesman_addorder'),
    
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/addtoorder', views.OrderItemCreateView.as_view(), name='product_addtoorder'),
    
    # Customer URLs
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),

    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/add', views.OrderCreateView.as_view(), name='order_add'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    # OrderItem URLs
    path('orderitems/<int:pk>/delete/', views.OrderItemDeleteView.as_view(), name='orderitem_delete'),
]
