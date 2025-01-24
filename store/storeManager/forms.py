from django import forms
from .models import Market, Salesman, Product, Customer, Order, OrderItem

class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['market_name', 'location']

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['salesman_name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'stock']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'email']
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer']
    
    customer = forms.ModelChoiceField(queryset=Customer.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'quantity']

    order = forms.ModelChoiceField(queryset=Order.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}),)

    def __init__(self, *args, **kwargs):
        product_stock = kwargs.pop('product_stock', None)
        super().__init__(*args, **kwargs)
        if product_stock:
            self.fields['quantity'].max_value = product_stock
            self.fields['quantity'].widget.attrs['max'] = product_stock