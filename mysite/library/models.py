from django.db import models
from django.contrib.auth.models import User

# Django Automatically generate ID
# when create user automatic create Student or faculty models or
class Users(models.Model):
    # extend the user from allauth
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    # In user already have firstname lastname
    phoneNumber = models.CharField(max_length=10)
    department = models.CharField(max_length=255)
    USER_CHOICES = (
        ('Student', 'Student'),
        ('Facalty', 'Facalty'),
    )
    userType = models.CharField(max_length=50, choices=USER_CHOICES, default='Student')

    def book_borrowed(self):
        book_borrow = Borrow.objects.filter(userID=self.userID)
        return [borrow.bookID for borrow in book_borrow]

    def __str__(self):
        return self.userID.first_name

class Authors(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    def __str__(self):
        return self.firstname

class Books(models.Model):
    title = models.CharField(max_length=255)
    authorID = models.ForeignKey(Authors, on_delete=models.CASCADE)
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


class Borrow(models.Model):
    userID = models.ForeignKey(Users,on_delete=models.CASCADE,default=None)
    bookID = models.ForeignKey(Books,on_delete=models.CASCADE)
    borrowDate = models.DateField()
    dueDate = models.DateField()
    returnDate = models.DateField(null=True)

    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Checked Out', 'Checked Out'),
        ('Reserved', 'Reserved'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"book:{self.bookID},borrower:{self.userID}"

class Fines(models.Model):
    borrowID = models.ForeignKey(Borrow, on_delete=models.CASCADE,default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    dateIssued = models.DateField()
    datePaid = models.DateField()