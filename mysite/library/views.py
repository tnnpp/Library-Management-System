from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import datetime


def home(request):
    return render(request, 'library/home.html')

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        results = Books.objects.filter(ISBN__title__contains=query)
        return render(request, 'library/search.html', {'results': results})


class DetailView(generic.DetailView):
    model = Books
    template_name = 'library/book.html'

    def get_queryset(self):
        return Books.objects.all()

@login_required()
def borrowbook(request, books_id):
    book = get_object_or_404(Books,pk=books_id)
    user = get_object_or_404(Users,userID=request.user)
    # check if user can borrow book or not
    if not book.can_borrow():
        messages.error(request, "The books is not available.")
        return render(request, 'library/book.html', {'books': book})
    for i in user.book_borrowed():
        if books_id == i.bookID :
            messages.error(request, "You already borrow this book.")
            return render(request, 'library/book.html', {'books': book})
    due_date = datetime.date.today() + datetime.timedelta(days=7)
    # Create a new Borrow object
    borrow = Borrow(userID=user, bookID=book, borrowDate=datetime.date.today(), dueDate=due_date, status='Borrowed')
    borrow.save()
    book.status = 'Borrowed'
    book.save()
    messages.success (request, "Borrowing Success!")
    return render(request, 'library/book.html', {'books': book})

@login_required()
def return_book(request, books_id):
    book = get_object_or_404(Books, pk=books_id)
    user = get_object_or_404(Users, userID=request.user)
    query = user.book_borrowed
    if book.can_borrow():
        messages.error(request,"You didn't borrowed this book.")
    messages.success(request, "Returning Success!")
    borrow = get_object_or_404(Borrow,bookID=book,status='Borrowed')
    if borrow.status == 'Returned':
        messages.error(request, "You have return this book")
    borrow.returnDate = datetime.date.today()
    borrow.status = 'Returned'
    borrow.save()
    book.status = 'Available'
    book.save()
    return render(request, 'library/my-books.html', {'borrows':query, 'user':user})


@login_required()
def mybook(request):
    user = get_object_or_404(Users, userID=request.user)
    query = user.book_borrowed
    return render(request, 'library/my-books.html', {'borrows':query, 'user':user})