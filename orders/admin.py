from django.contrib import admin
from .models import Order 
from .models import OrderItem
from django.urls import reverse
import csv
import datetime
from django.http import HttpResponse
from django.utils.safestring import mark_safe


def export_to_csv(modeladmin, request, queryset):
    opt = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
        filename={}.csv'.format(opt.verbose_name)
    writer = csv.writer(response)
    #create array of fields.
    fields = [field for field in opt.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to csv'

'''
The below method, order_detail has the following problem that needs fixing.
    "<class 'orders.admin.OrderAdmin'>: (admin.E108) The value of 'list_display[9]'
    refers to 'order_detail', which is not a callable, an attribute of 'OrderAdmin', 
    or an attribute or method on 'orders.Order'."
'''

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product',]

class OrderAdmin(admin.ModelAdmin):
    @mark_safe
    def order_pdf(self, obj):
        return '<a href="{}">PDF</a>'.format(reverse('adminOrderPdf', args=[obj.id]))
    order_pdf.allow_tags = True
    order_pdf.short_description = 'PDF bill'
    
    @mark_safe
    def order_detail(self, obj):
        return '<a href="{}">View</a>'.format(reverse('adminOrderDetail', args=[obj.id]))
    order_detail.allow_tags = True 
    
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated', 'order_detail', 'order_pdf',]
    list_filter = ['paid', 'created', 'updated',]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
admin.site.register(Order, OrderAdmin)
    
