from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',csrf_exempt(home),name='home'),
    path('user/',csrf_exempt(userPage),name='user'),
    path('account/',csrf_exempt(accountSettings),name='account-settings'),
    path('customers/<int:pk>/',csrf_exempt(customers),name='customer'),
    path('createcustomer/',csrf_exempt(AddCustomer),name='add-customer'),
    path('updatecustomer/<int:pk>/',csrf_exempt(UpdateCustomer),name='update-customer'),
    path('products/',csrf_exempt(products),name='products'),
    path('products/<str:pk>',csrf_exempt(updateproducts),name='products-update'),
    path('charts/',csrf_exempt(charts),name='charts'),
    path('getcharts/',csrf_exempt(getcharts),name='getcharts'),
    path('getcustomerchart/<int:pk>/',csrf_exempt(getcustomerchart),name='getcustomerchart'),
    path('create-order/<int:pk>/',csrf_exempt(createOrder),name='create-order'),
    path('update-order/<int:pk>/',csrf_exempt(updateOrder),name='update-order'),
    path('delete/<int:pk>/',csrf_exempt(deleteOrder),name='delete-order'),
    path('register/',csrf_exempt(registerPage),name='register'),
    path('login/',csrf_exempt(loginPage),name='login'),
    path('logout/',csrf_exempt(logoutUser),name='logout'),

    path('count/', Priotizing),

    path('categorize/', Categorizing),
]
