import json
from datetime import timedelta, date

from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from capital.models import Book, Transactions, Student, Payment


# Create your views here.
def dashboard(request):
    return render(request, template_name='dashboard.html')


def books_in_store(request):
    notes = Book.objects.all()

    return render(request, template_name='books_in_store.html', context={'notes':notes})


def borrowed_books(request):
    borrowed =Transactions.objects.all()
    return render(request, template_name='borrowed_books.html', context={'borrowed_items':borrowed})


def book_fines(request):
    transactions = Transactions.objects.all()
    fines =[t for t in transactions if t.total_fine>0] # t represents a single transaction
    return render(request, template_name='book_fines.html',context={'fines':fines})


def issue_book(request, id):

    book = Book.objects.get(pk=id)
    trainees = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST['student_id']
        student = Student.objects.get(pk=student_id)
        expected_return_date = date.today() + timedelta(days=7)
        transaction = Transactions.objects.create(book=book, student=student, expected_return_date=expected_return_date ,status='BORROWED')
        transaction.save()
        messages.success(request, f'Book {book.title} was borrowed successfully')
        return redirect('books_in_store')
    return render(request,template_name='issue.html',context={'book':book,'trainees':trainees})


def return_book(request, id):
    transaction = Transactions.objects.get(pk=id)
    transaction.return_date = date.today()
    transaction.status = 'RETURNED'
    messages.success(request, f'Book {transaction.book.title} was returned')
    if transaction.total_fine> 0:
        messages.warning(request, f'Book {transaction.book.title} was returned')
    return redirect('books_in_store')


def pay_overdue(request ,id):
    transaction = Transactions.objects.get(pk=id)
    total = transaction.total_fine
    phone = transaction.student.phone
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0798017611'
    amount = 1
    account_reference = transaction.student.adm_no
    transaction_desc = 'fines'
    callback_url = 'https://termite-key-cow.ngrok-free.app'  # copy code from ngrok
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    if response.response_code == 0:
        payment = Payment.objects.create(transaction=transaction,merchant_request_id=response.merchant_request_id,checkout_request_id= response.checkout_request_id, amount=amount)
        payment.save()
        messages.success(request, f'Payment of {transaction.book.title} was paid')
    return redirect('book_fines')

@csrf_exempt
def callback(request):
    resp = json.loads(request.body)
    data = resp['Body']['stkCallback']
    if data["ResultCode"] == "0":
        m_id = data["MerchantRequestID"]
        c_id = data["CheckoutRequestID"]
        code = ""
        item = data["CallbackMetadata"]["Item"]
        for i in item:
            name=i["Name"]
            if name == "MpesaReceiptNumber":
                code=i["Value"]
            transaction = Transactions.objects.get(merchant_request_id=m_id, checkout_request_id=c_id)
            transaction.code=code
            transaction.status="COMPLETED"
            transaction.save()
    return HttpResponse("OK")


def pie_chart(request):
    orders = Transactions.objects.filter(created_at__year=2024)
    returned = orders.filter(status='RETURNED').count()
    lost = orders.filter(status='LOST').count()
    borrowed =orders.filter(status='BORROWED').count()
    return JsonResponse({
        "title": "Grouped By Status",
        "data": {
            "labels": ["Returned", "Borrowed", "Lost"],
            "datasets": [{
                "data": [returned, lost, borrowed],
                "backgroundColor": ['#4e73df', '#1cc88a', '#36b9cc'],
                "hoverBackgroundColor": ['#2e59d9', '#17a673', '#2c9faf'],
                "hoverBorderColor": "rgba(234, 236, 244, 1)",
            }],
        }
    })
# the above code we find it in the jslink in dashboardhtml

def line_chart(request):
    orders = Transactions.objects.filter(created_at__year=2024)
    grouped = orders.annotate(month=TruncMonth('created_at')).values('month').annotate(
        count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime("%b"))
    return JsonResponse({
        "title": "Transactions Grouped By Month",
        "data": {
            "labels":["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "datasets": [{
                "label": months,
                "lineTension": 0.3,
                "backgroundColor": "rgba(78, 115, 223, 0.05)",
                "borderColor": "rgba(78, 115, 223, 1)",
                "pointRadius": 3,
                "pointBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointBorderColor": "rgba(78, 115, 223, 1)",
                "pointHoverRadius": 3,
                "pointHoverBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointHoverBorderColor": "rgba(78, 115, 223, 1)",
                "pointHitRadius": 10,
                "pointBorderWidth": 2,
                "data":numbers,
            }],
        },

    })



def bar_chart(request):
    transactions = Transactions.objects.filter(created_at__year=2024)
    grouped = transactions.annotate(month=TruncMonth('created_at')).values('month').annotate(
        count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime('%b'))
    print(months)
    return JsonResponse({
        "title": "Transactions Grouped By Month",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Total",
                "backgroundColor": "#4e73df",
                "hoverBackgroundColor": "#2e59d9",
                "borderColor": "#4e73df",
                "data": numbers,
            }],
        },
    })


def lost_book(request, id):
    transactions = Transactions.objects.get(id=id)
    transactions.status = 'LOST'
    transactions.return_date = date.today()
    transactions.save()
    messages.error(request, 'Book registered as lost!')
    return redirect('borrowed_books')