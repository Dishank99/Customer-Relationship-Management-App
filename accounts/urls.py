from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',csrf_exempt(home),name='home'),
    path('user/',csrf_exempt(userPage),name='user'),
    path('account/',csrf_exempt(accountSettings),name='account-settings'),
    path('customers/<int:pk>/',csrf_exempt(customers),name='customer'),
    path('products/',csrf_exempt(products),name='products'),
    path('products/<str:pk>',csrf_exempt(updateproducts),name='products-update'),
    path('charts/',csrf_exempt(charts),name='charts'),
    path('getcharts/',csrf_exempt(getcharts),name='getcharts'),
    path('create-order/<int:pk>/',csrf_exempt(createOrder),name='create-order'),
    path('update-order/<int:pk>/',csrf_exempt(updateOrder),name='update-order'),
    path('delete/<int:pk>/',csrf_exempt(deleteOrder),name='delete-order'),
    path('register/',csrf_exempt(registerPage),name='register'),
    path('login/',csrf_exempt(loginPage),name='login'),
    path('logout/',csrf_exempt(logoutUser),name='logout'),
]
