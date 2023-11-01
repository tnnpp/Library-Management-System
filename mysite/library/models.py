from django.db import models
from django.contrib.auth.models import User

# Django Automatically generate ID
# when create user automatic create Student or faculty models or
class Students(models.Model):
    # extend the user from allauth
    studentID = models.ForeignKey(User,on_delete=models.CASCADE)
    # In user already have firstname lastname
    phoneNumber = models.CharField(max_length=10)
    department = models.CharField(max_length=255)

    def book_borrowed(self):
        book_borrow = Borrow.objects.filter(studentID=self.studentID)
        return [borrow.bookID for borrow in book_borrow]


class Faculty(models.Model):
    # extent user
    faculty_id = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    facultyName = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

class Authors(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    def writed_books(self):
        return self.books_set

    def __str__(self):
        return  self.title

class Books(models.Model):
    title = models.CharField(max_length=255)
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=13)
    yearPublished = models.IntegerField()
    genre = models.CharField(max_length=255)
    shelfLocation = models.CharField(max_length=255)
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Checked Out', 'Checked Out'),
        ('Reserved', 'Reserved'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return  self.title

class BookIssues(models.Model):
    bookID = models.ForeignKey(Books, on_delete=models.CASCADE)
    issuerID = models.IntegerField()
    dueDate = models.DateField()
    returnDate = models.DateField()
    ISSUER_CHOICES = (
        ('Student', 'Student'),
        ('Facalty', 'Facalty'),
    )
    issuerType = models.CharField(max_length=50,choices=ISSUER_CHOICES,default='Available')

    def __str__(self):
        return f"book:{self.bookID},Issuer:{self.issuerID}"

class Borrow(models.Model):
    issuerID = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    bookID = models.ForeignKey(Books,on_delete=models.CASCADE)
    borrowDate = models.DateField()
    dueDate = models.DateField()
    returnDate = models.DateField(null=True)

    ISSUER_CHOICES = (
        ('Student', 'Student'),
        ('Facalty', 'Facalty'),
    )
    issuerType = models.CharField(max_length=50, choices=ISSUER_CHOICES,default='Available')
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Checked Out', 'Checked Out'),
        ('Reserved', 'Reserved'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"book:{self.bookID},borrower:{self.issuerID}"

class Fines(models.Model):
    fineID = models.IntegerField()
    issueID = models.ForeignKey(BookIssues, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    dateIssued = models.DateField()
    datePaid = models.DateField()