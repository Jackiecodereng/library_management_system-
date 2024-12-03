"""
URL configuration for library_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf

    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from capital import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books', views.books_in_store, name='books_in_store'),
    path('borrowed_books', views.borrowed_books, name='borrowed_books'),
    path('fines', views.book_fines, name='book_fines'),
    path('issue/<int:id>', views.issue_book, name='issue_books'),
    path('return/<int:id>', views.return_book, name='return_book'),
    path('pay/<int:id>', views.pay_overdue, name='pay_overdue'),
    path('handle/payment/transactions', views.callback, name='callback'),
    path('pie-chart', views.pie_chart, name='pie_chart'),
    path('line-chart', views.line_chart, name='line_chart'),
    path('bar-chart', views.bar_chart, name='bar_chart'),
   path('lost/book/<int:id>', views.lost_book, name='lost_book'),
    path('admin/', admin.site.urls),
]
