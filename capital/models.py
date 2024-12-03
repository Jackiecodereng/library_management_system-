from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=15)
    adm_no = models.CharField(unique=True, max_length=15)

    def __str__(self):
        return f"{self.name} - {self.adm_no}"
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['adm_no']
        db_table = 'trainees'

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    subject = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.title} - {self.isbn}"
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['isbn']
        db_table = 'notes'

class Transactions(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    expected_return_date = models.DateField()
    return_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.book} - {self.student}"

    @property
    def total_fine(self):
        if self.return_date and self.expected_return_date and self.return_date > self.expected_return_date:
            amount = (self.return_date-self.expected_return_date).days*10
            return amount
        return 0
    @property
    def overdue_days(self):
        if self.return_date and self.expected_return_date and self.return_date > self.expected_return_date:
            days = (self.return_date-self.expected_return_date).days
            return days
        return 0
    class Meta:
        verbose_name = 'Transactions'
        verbose_name_plural = 'Transactions'
        ordering = ['created_at']
        db_table = 'orders'

class Payment(models.Model):
    transactions = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    code = models.CharField(max_length=30,null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20,default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.code} - {self.merchant_request_id}-{self.amount}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        db_table = 'payments'

#ALTER DATABASE `library_db` CHARACTER SET utf8; -hrelps solve this error in my sql then drop all the tables


