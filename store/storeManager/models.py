from django.db import models
from django.contrib.auth.models import AbstractUser

class Market(models.Model):
    market_id = models.AutoField(primary_key=True)
    market_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.market_name

class Salesman(models.Model):
    salesman_id = models.AutoField(primary_key=True)
    salesman_name = models.CharField(max_length=255)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self):
        return self.salesman_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product_name

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.customer_name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_created=True, auto_now=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE, null=True, blank=True)
    total_value = models.IntegerField(default=0)

    def __str__(self):
        return f"Order {self.order_id}"

class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    stock_state = models.BooleanField(default=False)

    def __str__(self):
        return f"Item {self.item_id}"
