from django.shortcuts import render
from .models import Book, Person
from datetime import date

# Create your views here.
def home(request):
    # pass Books and people from  database to template
    books = Book.objects.all()
    people = Person.objects.all().count()

    # keeps count of how many books are checked out, late, and due today
    late = 0
    due_today = 0

    # counts how many books are late and due today
    today = date.today()
    today = int(str(today.year)+str(today.month).zfill(2)+str(today.day).zfill(2))
    for book in books.filter(available=False):
        if today > int(book.due_date):  # count how many books are late
            late = late + 1
        if today == int(book.due_date):  # count how many books are due today
            due_today = due_today + 1
    checked_out = books.filter(available=False).count() - due_today - late
    context ={
        'books': books,
        'person': people,
        'out': checked_out,
        'late': late,
        'today': due_today,
        'Home': "active",
    }
    return render(request, 'active_template/index.html', context)

def checkedout_books(request):
    today = date.today()
    todays_date = int(str(today.year)+str(today.month).zfill(2)+str(today.day).zfill(2))
    books_out = Book.objects.filter(available=False).order_by('due_date')

    context = {
        'books_out': books_out,
        'today': todays_date
    }
    return render(request, 'active_template/checkedout.html', context)

def due_today(request):
    today = date.today()
    todays_date = int(str(today.year)+str(today.month).zfill(2)+str(today.day).zfill(2))
    due = Book.objects.filter(due_date=todays_date)
    return render(request, 'active_template/duetoday.html', {'due': due})

def overdue(request):
    today = date.today()
    todays_date = int(str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2))
    overdue = Book.objects.filter(available=False).order_by('-due_date')

    context = {
        'overdue': overdue,
        'today': todays_date
    }
    return render(request, 'active_template/overdue.html', context)

def help(request):
    return render(request, 'active_template/help.html', {'Help': 'active'})