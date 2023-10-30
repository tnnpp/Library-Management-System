from django.db import models
from django.contrib.auth.models import User

# Django Automatically generate ID
class Students(models.Model):
    # extend the user from allauth
    studentID = models.ForeignKey(User,on_delete=models.CASCADE())
    firstName = models.ForeignKey(User.first_name,on_delete=models.CASCADE)
    lastName = models.ForeignKey(User.last_name,on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=10)
    email = models.ForeignKey(User.email,on_delete=models.CASCADE)
    department = models.CharField(max_length=255)

    def book_borrowed(self):
        book_borrow = Borrow.objects.filter(studentID=self.studentID)
        return [borrow.bookID for borrow in book_borrow]

class Faculty(models.Model):
    facultyName = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

class Authors(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

class Books(models.Model):
    title = models.CharField(max_length=255)
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=13)
    yearPublished = models.IntegerField()
    genre = models.CharField(max_length=255)
    shelfLocation = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def is_Status(self):
        return self.status in ['Available', 'Checked Out', 'Reserved']

class BookIssues(models.Model):
    bookID = models.ForeignKey(Books, on_delete=models.CASCADE)
    issuerID = models.IntegerField()
    dueDate = models.DateField()
    returnDate = models.DateField()
    issuerType = models.CharField(max_length=50)

    def is_issuer(self):
        return self.issueType in ['Student', 'Facalty']

class Borrow(models.Model):
    studentID = models.ForeignKey(Students,on_delete=models.CASCADE)
    bookID = models.ForeignKey(Books,on_delete=models.CASCADE)
    borrowDate = models.DateField()
    dueDate = models.DateField()
    returnDate = models.DateField(null=True)
    BorrowerType = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def is_Borrower(self):
        return self.BorrowerType in ['Student', 'Facalty']

    def is_status(self):
        return self.status in ["returned","not return"]

class Fines(models.Model):
    fineID = models.IntegerField()
    issueID = models.ForeignKey(BookIssues, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    dateIssued = models.DateField()
    datePaid = models.DateField()