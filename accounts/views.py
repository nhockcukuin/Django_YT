from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
from .form import OrderForm, CreateUserForm
from .filters import OrderFilter

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"user name or pass is incorrect")
    context = {}
    return render(request,'accounts/login.html',context)

def registerPage(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,"Account was created for " + user)
            return redirect('login')
    context = {'form':form}
    return render(request,'accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
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

@login_required(login_url='login')
def products(request):
    products = Products.objects.all()
    return render(request,'accounts/products.html',{'products': products})

@login_required(login_url='login')
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    order = customer.order_set.all()
    order_count = order.count()
    myFilter = OrderFilter(request.GET,queryset=order)
    order = myFilter.qs
    context = {'customer':customer,'order':order,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('products','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer': customer})
    formset = OrderFormSet(instance=customer)
    if request.method =='POST':
        # print('Printing POST',request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(order = Order.objects.none(),instance=order)
    if request.method =='POST':
        # print('Printing POST',request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk) 
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'accounts/deleteform.html',context)
