from django.http import HttpResponse
from django.shortcuts import render, redirect

#decorator that will stop an authenticated user to view login and register page
def restrict_auth_user(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return func(request, *args, **kwargs)
        
    return wrapper_func

#decorator that will varify the allowed roles with thw  group user is part of
def allowed_users(allowed_roles=[]):
    def decorator_func(func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists(): 
                group = request.user.groups.all()[0].name
            #print(type(group))
            if group in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page', status=403)
        return wrapper_func
    return decorator_func

#decorator that reoutes customer to userpage and admin to homepage
def admin_only(func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name 

        if group == 'customer':
            return redirect('user')
        elif group== 'admin':
            return func(request, *args, **kwargs)

    return wrapper_func

