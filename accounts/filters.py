from .models import *
import django_filters
from django_filters import DateFilter

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = [
            'product',
            'status',
        ]

class OrderChartFilter(django_filters.FilterSet):
    start_date = DateFilter(label = 'From ', field_name = 'date_created', lookup_expr='gte')
    end_date = DateFilter(label = 'Till ', field_name = 'date_created', lookup_expr='lte')
    class Meta:
        model = Order
        fields = ''        
