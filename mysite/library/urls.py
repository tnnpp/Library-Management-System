from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.DetailView.as_view(), name='book'),
    path('<int:books_id>/borrow/', views.borrowbook, name='borrow'),
    path('mybook/', views.mybook, name='mybook'),
    path('<int:books_id>/return/', views.return_book, name='return'),
    path('<int:borrow>/paid/',views.fine_paid, name='paid')
   ]
