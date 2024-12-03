from django.contrib import admin

from capital.models import Student, Book, Transactions, Payment


# Register your models here.
admin.site.site_header = 'Library MIS'
admin.site.site_title = 'Library Management System'
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','adm_no']
    search_fields = ['name','email','phone','adm_no']
    list_per_page = 30

class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','year','isbn','subject']
    search_fields = ['title', 'author', 'year', 'isbn', 'subject']
    list_per_page = 35

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['book','status','expected_return_date']
    search_fields = ['book', 'status', 'expected_return_date']
    list_per_page = 25

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transactions','code','status','amount','created_at']
    search_fields = ['transactions','code','status','amount','created_at']
    list_per_page = 25

admin.site.register(Student,StudentAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Transactions,TransactionAdmin)
admin.site.register(Payment,PaymentAdmin)

#python manage.py createsuperuser
#username/email: admin1@gmail.com
#password:123456


