from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from .categorizing_customer import *

from django.http import JsonResponse

@restrict_auth_user
def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            messages.success(request,f'User {username} created successfully')
            return redirect('login')        
        messages.error(request,form.errors)

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@restrict_auth_user
def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.info(request,'Username or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-date_created')
    print(orders)
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_orders_pending = orders.filter(status='Pending').count()
    total_orders_delivered = orders.filter(status='Delivered').count()

    context = {
        'orders':orders[:5],
        'customers':customers,
        'total_orders':total_orders,
        'total_orders_pending':total_orders_pending,
        'total_orders_delivered':total_orders_delivered,
    }
    return render(request,'accounts/dashboard.html',context)

@login_required
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    #orders = request.user.customer.order_set.all()
    orders = Order.objects.filter(customer = request.user.customer)
    total_orders = orders.count()
    total_orders_delivered = orders.filter(status='Delivered').count()
    total_orders_pending = orders.filter(status='Pending').count()
    context = {
        'orders_by_customer':orders,
        'total_orders':total_orders,
        'total_orders_delivered':total_orders_delivered,
        'total_orders_pending':total_orders_pending,
    }
    return render(request, 'accounts/user.html', context)

@login_required
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = Customer.objects.get(user = request.user)
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES, instance = customer)
        if form.is_valid():
            form.save()
            return redirect('user')
    print(type(form))
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    # orders_by_customer = Order.objects.all().filter(customer=customer)
    orders_by_customer = customer.order_set.all()
    my_Filter = OrderFilter(request.GET, queryset=orders_by_customer)
    orders_by_customer_filtered = my_Filter.qs
    context = {
        'my_Filter':my_Filter,
        'customer':customer,
        'orders_by_customer':orders_by_customer_filtered,
        'orders_by_customer_count':orders_by_customer.count(),
    }
    print(context)
    return render(request,'accounts/customers.html',context)

# @login_required
# @allowed_users(allowed_roles=['admin'])
# def products(request):
#     products = Product.objects.all()
#     form = ProductForm()

#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('products')

#     return render(request,'accounts/products.html',{'products':products, 'form':form})

@login_required
@allowed_users(allowed_roles=['admin'])
def products(request, pk=None):
    products = Product.objects.all()
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')

    return render(request,'accounts/products.html',{'products':products, 'form':form})

@login_required
@allowed_users(allowed_roles=['admin'])
def updateproducts(request, pk=None):
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    return render(request,'accounts/product_form.html',{'product':product, 'form':form})

@login_required
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    print(customer)
    formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        #print(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect('home')

orders_filtered=None
@login_required
@allowed_users(allowed_roles=['admin'])
def charts(request):
    global orders_filtered
    orders = Order.objects.all()
    my_Filter = OrderChartFilter(request.GET, queryset=orders)
    orders_filtered = my_Filter.qs
    return render(request, 'accounts/charts.html',{'my_Filter':my_Filter})

def getcharts(request):
    #order = order.objects.all()
    product = Product.objects.all()
    productlabels = [p.name for p in product]
    productdata = [p.order_set.count() for p in product]

    customer = Customer.objects.all()
    customerlabels = [c.name for c in customer]
    customerdata = [co.order_set.count() for co in customer]

    orders = Order.objects.all()
    # my_Filter = OrderChartFilter(request.GET, queryset=orders)
    # orders_filtered = my_Filter.qs
    oclabels = sorted(list(set([str(oc.date_created).split(' ')[0] for oc in orders])))
    #ocdata = [i for i in range(orders_filtered.count())]
    ocdata=[]
    for ocdate in oclabels:
        #date = str(oc.date_created).split(' ')[0]
        print(ocdate)
        count=0
        for j in range(len(orders)):
            if str(orders[j].date_created).split(' ')[0] == ocdate:
                count += 1
        print(count)
        ocdata.append(count)

    print(oclabels)

    data = {
        'customer' : {
                            'labels':customerlabels,
                            'data':customerdata,
                        },    
        'product' : {
                        'labels':productlabels,
                        'data':productdata,
                    },
        'order_customer' : {
                                'labels':oclabels,
                                'data':ocdata,
                            },
            }
        
    return JsonResponse(data)

def getcustomerchart(request, pk):
    customer = Customer.objects.get(pk=pk)    

    orders = customer.order_set.all()
    # my_Filter = OrderChartFilter(request.GET, queryset=orders)
    # orders_filtered = my_Filter.qs
    oclabels = sorted(list(set([str(oc.date_created).split(' ')[0] for oc in orders])))
    #ocdata = [i for i in range(orders_filtered.count())]
    ocdata=[]
    for ocdate in oclabels:
        #date = str(oc.date_created).split(' ')[0]
        print(ocdate)
        count=0
        for j in range(len(orders)):
            if str(orders[j].date_created).split(' ')[0] == ocdate:
                count += 1
        print(count)
        ocdata.append(count)

    print(oclabels)

    data = {
        'order_customer' : {
                                'labels':oclabels,
                                'data':ocdata,
                            },
            }
        
    return JsonResponse(data)

@allowed_users(allowed_roles=['admin'])
def AddCustomer(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'accounts/customeradmin.html', {'form':form})

@allowed_users(allowed_roles=['admin'])
def UpdateCustomer(request, pk):
    customer = Customer.objects.get(pk=pk)
    form = UpdateCustomerForm(instance=customer)

    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'accounts/account_settings.html', {'form':form})

def Priotizing(request):
    product_order_count = {}
    customer_order_count = {}

    for order in Order.objects.all():
        if order.customer is not None and order.product is not None:
            if order.customer.name in customer_order_count:
                customer_order_count[order.customer.name]['count'] += 1
            else:
                customer_order_count[order.customer.name] = {
                                                            'type':int(order.customer.category) if order.customer.category else 1,
                                                            'count':0
                                                            }
            if order.product.name in product_order_count:
                product_order_count[order.product.name] += 1
            else:
                product_order_count[order.product.name] = 0
        # print(customer_order_count)
    print(customer_order_count.items())
    customer_order_count = dict(sorted(customer_order_count.items(), key = lambda kv:(kv[1]['type'], kv[1]['count']), reverse=True))
    product_order_count = dict(sorted(product_order_count.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))

    misc = {
            'Customer_to_Order':customer_order_count, 
            'Product_to_Order':product_order_count
            }

    return JsonResponse(customer_order_count,safe=False)

def Categorizing(request):
    return JsonResponse(categorize_all(),safe=False)
