from .models import *

'''
if date of creation of product - date of order of product by customer < 2days then, customer is impulsive
if product has offer and customer ordered for that product then, customer is discount type
if no. of orders of customer is < 2 then, customer is new
else customer is loyal
'''

def categorize(customer_order):
    impulsive_count=0
    discount_count=0
    for co in customer_order:
        if co.product.offer != 0.0 and (co.date_created - co.product.offer_added).seconds/(60*60*24) < 2.0:
            discount_count += 1
            print(f'{co.customer.name}: {discount_count}')
        if (co.date_created - co.product.date_created).seconds/(60*60*24) < 2.0:
            impulsive_count += 1
    if discount_count > customer_order.count()/2:
        return '3'
    elif impulsive_count > customer_order.count()/(3/4):
        return '2'
    elif customer_order.count() < 2:
        return '1'
    else:
        return '4'
    
def categorize_all():
    json_resp=[]
    for c in Customer.objects.all():
        c.category = categorize(c.order_set.all())
        c.save()
        json_resp.append({
            c.name: c.category
        })
    
    return json_resp

def categorize_specific(customer):
    customer.category = categorize(customer.order_set.all())
    customer.save()
    return {customer: customer.category}
