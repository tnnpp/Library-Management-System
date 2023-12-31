from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Books,Users,Fines,BookInformation,Borrow
from django.views import generic
from django.urls import reverse
from django.contrib import messages
import datetime
from django.db import connection


def home(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT bi.title, COUNT(b.bookID_id) as borrow_count
            FROM library_borrow b
            JOIN library_books bk ON b.bookID_id = bk.id
            JOIN library_bookinformation bi ON bk.ISBN_id = bi.id
            GROUP BY b.bookID_id, bi.title
            ORDER BY borrow_count DESC
            LIMIT 3;
        """)
        results = cursor.fetchall()
        print(results)
    return render(request, 'library/home.html', {'popular_book': results})

def search(request):
    results=[]
    if request.method == 'POST':
        query = request.POST.get('query', '')
        categories = request.POST.get('categories', '')
        if categories == 'Status':
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT bi.title, b.id
                    FROM library_books b
                    JOIN library_bookinformation bi ON b.ISBN_id = bi.id
                    WHERE b.status = %s;
                """, [query])
                results = cursor.fetchall()
        if categories == "Author":
            if " " in query:
                name = query.split(" ")
                firstname = name[0]
                lastname = name[1]
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT bi.title, b.id
                        FROM library_bookInformation bi
                        JOIN library_authors a ON bi.authorID_id = a.id
                        JOIN library_books b ON b.ISBN_id = bi.id
                        WHERE a.firstName = %s and a.lastname = %s ;
                    """, (firstname, lastname))
                    results = cursor.fetchall()
                    print(firstname,lastname)
            else:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT bi.title, b.id
                        FROM library_bookInformation bi
                        JOIN library_authors a ON bi.authorID_id = a.id
                        JOIN library_books b ON b.ISBN_id = bi.id
                        WHERE a.firstName = %s ;
                    """, [query])
                    results = cursor.fetchall()
        if categories == "Title":
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT bi.title, b.id
                    FROM library_books b
                    JOIN library_bookinformation bi ON b.ISBN_id = bi.id
                    WHERE bi.title LIKE %s;
                """, [query + '%'])
                results = cursor.fetchall()

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
        return redirect(reverse('library:book', kwargs={'pk': books_id}))
    for i in user.book_borrowed():
        if books_id == i.bookID :
            messages.error(request, "You already borrow this book.")
            return redirect(reverse('library:book', kwargs={'pk': books_id}))
    due_date = datetime.date.today() + datetime.timedelta(days=7)
    # Create a new Borrow object
    borrow = Borrow(userID=user, bookID=book, borrowDate=datetime.date.today(), dueDate=due_date, status='Borrowed')
    borrow.save()
    book.status = 'Borrowed'
    book.save()
    messages.success (request, "Borrowing Success!")
    return redirect(reverse('library:book', kwargs={'pk': books_id}))

@login_required()
def return_book(request, books_id):
    book = get_object_or_404(Books, pk=books_id)
    user = get_object_or_404(Users, userID=request.user)
    query = user.book_borrowed()
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
    return redirect(reverse('library:mybook'), {'borrows':query, 'user':user})


@login_required()
def mybook(request):
    user = get_object_or_404(Users, userID=request.user)
    query = user.book_borrowed()
    # create fines object automaticly when go to the page
    if query:
        for borrow in query:
            if (datetime.date.today() > borrow.dueDate):
                fine = (datetime.date.today() - borrow.dueDate).days * 10
                if Fines.objects.filter(borrowID=borrow).exists():
                    fine_get = Fines.objects.get(borrowID=borrow)
                    fine_get.amount = fine
                    fine_get.save()
                    continue
                if borrow.returnDate > borrow.dueDate:
                    fine = (borrow.returnDate - borrow.dueDate).days * 10
                    fine_create = Fines.objects.create(borrowID=borrow, amount=fine, reason="Late return",
                                                       dateIssued=borrow.dueDate)
                    fine_create.save()
                    continue
                # if fine object is not created yet
                if (borrow.returnDate==None) :
                    fine_create = Fines.objects.create(borrowID=borrow, amount=fine, reason="Late return", dateIssued=borrow.dueDate)
                    fine_create.save()
    fines = Fines.objects.all()
    return render(request, 'library/my-books.html', {'borrows':query, 'user':user, 'fines':fines})

@login_required()
def fine_paid(request, borrow):
    fine_get = get_object_or_404(Fines, pk=borrow)
    fine_get.delete()
    user = get_object_or_404(Users, userID=request.user)
    query = user.book_borrowed
    fines = Fines.objects.all()
    return redirect(reverse('library:mybook'), {'borrows':query, 'user':user, 'fines':fines})

def Issue_page(request):
    results = []
    issue = ''
    if request.method == 'POST':
        issue = request.POST.get('issue', '')
        if issue == 'Pending':
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT a.first_name, a.last_name 
                    FROM library_users u
                    JOIN library_borrow bo ON u.id = bo.userID_id
                    JOIN library_fines f ON bo.id = f.borrowID_id
                    JOIN auth_user a ON u.userID_id = a.id
                    WHERE f.datePaid IS NULL;
                """)
                results = cursor.fetchall()
        if issue == 'not_return':
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT bi.title, b.id
                    FROM library_borrow AS br
                    JOIN library_books AS b ON br.bookID_id = b.id
                    JOIN library_bookinformation AS bi ON b.ISBN_id = bi.id
                    WHERE br.status = 'Borrowed' AND br.returnDate IS NULL;

                """)
                results = cursor.fetchall()
        if issue == 'overdue':
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT a.first_name, a.last_name, bi.title
                    FROM library_borrow bo
                    JOIN library_users u ON bo.userID_id = u.id
                    JOIN library_books b ON bo.bookID_id = b.id
                    JOIN library_bookInformation bi ON b.ISBN_id = bi.ISBN
                    JOIN auth_user a ON u.userID_id = a.id
                    WHERE bo.returnDate IS NULL AND bo.dueDate < %s;
                """, [datetime.date.today()])
                results = cursor.fetchall()
        print(results)
    return render(request, 'library/issue.html', {'results': results,'selected_issue': issue})
