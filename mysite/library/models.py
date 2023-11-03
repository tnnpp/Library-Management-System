from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Django Automatically generate ID
class Users(models.Model):
    # extend the user from allauth
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    # In user already have firstname lastname
    phoneNumber = models.CharField(max_length=10,null=True)
    department = models.CharField(max_length=255,null=True)
    USER_CHOICES = (
        ('Student', 'Student'),
        ('Facalty', 'Facalty'),
    )
    userType = models.CharField(max_length=50, choices=USER_CHOICES, default='Student')

    def book_borrowed(self):
        book_borrow = Borrow.objects.filter(userID=self)
        return [borrow for borrow in book_borrow]

    def __str__(self):
        return str(self.userID)

class Authors(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    def __str__(self):
        return self.firstname

class BookInformation(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    authorID = models.ForeignKey(Authors, on_delete=models.CASCADE)
    yearPublished = models.IntegerField()
    genre = models.CharField(max_length=255)

    def __str__(self):
        return  self.title

class Books(models.Model):
    ISBN = models.ForeignKey(BookInformation, on_delete=models.CASCADE)
    shelfLocation = models.CharField(max_length=255)
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Borrowed', 'Borrowed'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def can_borrow(self):
        return self.status == 'Available'

    def __str__(self):
        return self.ISBN.title


class Borrow(models.Model):
    userID = models.ForeignKey(Users,on_delete=models.CASCADE,default=None)
    bookID = models.ForeignKey(Books,on_delete=models.CASCADE)
    borrowDate = models.DateField()
    dueDate = models.DateField()
    returnDate = models.DateField(null=True)

    STATUS_CHOICES = (
        ('Borrowed', 'Borrowed'),
        ('returned', 'returned'),
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

    def __str__(self):
        return f"{self.borrowID}, amount:{self.amount}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(userID=instance, userType='Student', phoneNumber=None, department=None)
