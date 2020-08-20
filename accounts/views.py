from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import *

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders':orders,'customers': customers,'total_order':total_order,'delivered':delivered,'pending':pending
    }
    return render(request,'accounts/dashboard.html',context)


def products(request):
    products = Products.objects.all()
    return render(request,'accounts/products.html',{'products': products})


def customer(request):
    return render(request,'accounts/customer.html')