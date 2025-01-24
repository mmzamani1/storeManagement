from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Market, Salesman, Product, Customer, Order, OrderItem
from .forms import MarketForm, SalesmanForm, ProductForm, CustomerForm, OrderForm, OrderItemForm
from django.contrib import admin
from django.shortcuts import render

admin.site.register(Market)
admin.site.register(Salesman)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

def home(request):
    
    markets = Market.objects.all()
    salesmen = Salesman.objects.all()
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    orderitems = OrderItem.objects.all()
    
    return render(request, 'home.html', {
        'markets' : markets,
        'salesmen' : salesmen,
        'products' : products,
        'customers' : customers,
        'orders' : orders,
        'orderitems' : orderitems,
    })

# Generic views for Market
class MarketListView(ListView):
    model = Market
    template_name = 'market/market_list.html'
    context_object_name = 'markets'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Market.objects.filter(market_name__icontains=query)
        return Market.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['additional_objects'] = Salesman.objects.all()
        context['additional_objects2'] = Customer.objects.all()
        
        return context

class MarketCreateView(CreateView):
    model = Market
    form_class = MarketForm
    template_name = 'market/market_form.html'
    success_url = reverse_lazy('market_list')

class MarketUpdateView(UpdateView):
    model = Market
    form_class = MarketForm
    template_name = 'market/market_form.html'
    success_url = reverse_lazy('market_list')

class MarketDeleteView(DeleteView):
    model = Market
    template_name = 'market/market_confirm_delete.html'
    success_url = reverse_lazy('market_list')

# Salesman Views
class SalesmanListView(ListView):
    model = Salesman
    template_name = 'salesman/salesman_list.html'
    context_object_name = 'salesmen'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Salesman.objects.filter(salesman_name__icontains=query)
        return Salesman.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        
        context['additional_objects'] = Product.objects.all()
        context['additional_objects2'] = Order.objects.all()
        
        return context

class SalesmanCreateView(CreateView):
    model = Salesman
    form_class = SalesmanForm
    template_name = 'salesman/salesman_form.html'
    success_url = reverse_lazy('market_list')
    
    def form_valid(self, form):
        
        marketId = self.kwargs['pk']
        form.instance.market_id = marketId
        
        return super().form_valid(form)

class SalesmanUpdateView(UpdateView):
    model = Salesman
    form_class = SalesmanForm
    template_name = 'salesman/salesman_form.html'
    success_url = reverse_lazy('market_list')

class SalesmanDeleteView(DeleteView):
    model = Salesman
    template_name = 'salesman/salesman_confirm_delete.html'
    success_url = reverse_lazy('market_list')

# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(product_name__icontains=query)
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        
        context['additional_objects'] = OrderItem.objects.all()
        
        return context 
    
    def setup(self, request, *args, **kwargs):
        
        products = Product.objects.all()
        
        for product in products:
            orderitems = OrderItem.objects.filter(product=product)
            
            for orderitem in orderitems:
                if orderitem.stock_state == False:
                    product.stock = product.stock - orderitem.quantity
                    orderitem.stock_state = True
                    orderitem.save()
                    
            product.save()
        
        return super().setup(request, *args, **kwargs)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('salesman_list')
    
    def form_valid(self, form):
        salesmanId = self.kwargs['pk']
        related_salesman = Salesman.objects.get(pk=salesmanId)
        related_market = related_salesman.market
        
        form.instance.salesman_id = salesmanId
        form.instance.market = related_market
        
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# Customer Views
class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Customer.objects.filter(customer_name__icontains=query)
        return Customer.objects.all()

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')
    
    def form_valid(self, form):
        marketId = self.kwargs['pk']
        
        form.instance.market_id = marketId
        
        return super().form_valid(form)
    

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

# Order Views
class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Order.objects.filter(customer__customer_name__icontains=query)
        return Order.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['additional_objects'] = OrderItem.objects.all()
        
        return context
    
    def setup(self, request, *args, **kwargs):
        
        orders = Order.objects.all()
        total_value = 0
        
        for order in orders:
            orderitems = OrderItem.objects.filter(order=order)
            
            for orderitem in orderitems:
                p = Product.objects.get(pk=orderitem.product.pk)   
                total_value += (p.price * orderitem.quantity)
                order.total_value = total_value
                order.save()
                
            if not orderitems:
                order.total_value = 0
                order.save()
        
        return super().setup(request, *args, **kwargs)
    
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('order_list')
    
    def form_valid(self, form):
        salesmanId = self.kwargs['pk']
        
        related_salesman = Salesman.objects.get(pk=salesmanId)
        related_market = related_salesman.market
        
        form.instance.salesman = related_salesman
        form.instance.market = related_market
        
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        salesmanId = self.kwargs['pk']
        related_salesman = Salesman.objects.get(pk=salesmanId)
        related_market = related_salesman.market
        
        form.fields['customer'].queryset = Customer.objects.filter(market=related_market)
        
        return form
    

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
    
    def setup(self, request, *args, **kwargs):
        
        orders = Order.objects.all()
        for order in orders:
            
            products = Product.objects.all()
            
            for product in products:
                orderitems = OrderItem.objects.filter(product=product, order=order)
                
                for orderitem in orderitems:
                    if orderitem.stock_state == True:
                        product.stock = product.stock + orderitem.quantity
                        orderitem.stock_state = False
                        orderitem.save()
                
                product.save()
            
        return super().setup(request, *args, **kwargs)

# OrderItem Views

class OrderItemCreateView(CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'orderitem/orderitem_form.html'
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):

        productId = self.kwargs['pk']
        related_product = Product.objects.get(pk=productId)
        form.instance.product = related_product
        
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        
        form = super().get_form(form_class)
        
        product_id = self.kwargs['pk']
        related_product = Product.objects.get(pk=product_id)
        related_salesman = related_product.salesman
        related_market = related_product.market
        quantity = related_product.stock

        form.fields['order'].queryset = Order.objects.filter(salesman=related_salesman, market=related_market)
        form.fields['quantity'].widget.attrs['max'] = quantity  
        form.fields['quantity'].max_value = quantity            

        return form
    
class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = 'orderitem/orderitem_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    
    def setup(self, request, *args, **kwargs):
        
        products = Product.objects.all()
        
        for product in products:
            orderitems = OrderItem.objects.filter(product=product)
            
            for orderitem in orderitems:
                if orderitem.stock_state == True:
                    product.stock = product.stock + orderitem.quantity
                    orderitem.stock_state = False
                    orderitem.save()
            
            product.save()
        
        return super().setup(request, *args, **kwargs)
