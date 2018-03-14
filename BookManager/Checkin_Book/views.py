from django.shortcuts import render
from Database.models import Book, Person
from Database.forms import Createbook, CreateUser
from datetime import date
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def checkin_books_individually(request):
    books_out = Book.objects.filter(available=False)
    query = request.GET.get("q")  # set the search term in the query var
    checkin_pk = request.POST.get("book_pk")
    if query:  # if there is a search term, apply these filters to the books
        books_out = books_out.filter(
            Q(title__icontains=query)|
            Q(author__icontains=query)|
            Q(call_id__icontains=query)
        )
    paginator = Paginator(books_out, 12)  # sets what to paginate and how many per page
    page_var = "page"  # used when multiple pages to get books on x page
    page = request.GET.get(page_var)
    try:  # if a page is passed...
        queryset = paginator.page(page)  # tries to get that page
    except PageNotAnInteger:  # if page is not a number...
        queryset = paginator.page(1)  # returns the first page
    # except EmptyPage:  # if page number is empty...
    #    queryset = paginator.page(paginator.num_pages)  # returns the last page available
    
    if checkin_pk:
        book = Book.objects.get(pk=checkin_pk)
        person = Person.objects.get(id=book.holder.id)
        person.books_out = person.books_out - 1
        book.available = True
        book.due_date = None
        book.days_to_be_out = 0
        book.holder = None
        person.save()
        book.save()
        return redirect('checkin')

    return render(request, 'checkin.html', {'books_out': queryset, 'page_var':page_var, 'Checkin': 'active'})

def checkin_by_user(request):
    users = Person.objects.exclude(books_out=0)
    query = request.GET.get('q')
    if query:
        users = users.filter(
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)|
            Q(full_name__icontains=query)|
            Q(id_number__icontains=query)
        )
    paginator = Paginator(users, 10)
    page_var = 'page'
    page = request.GET.get(page_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)

    return render(request, 'checkin-individual.html', {'users': queryset, 'page_var': page_var, 'Checkin': 'active'})

def checkin_user_books(request, pk):
    user = get_object_or_404(Person, pk=pk)
    user_books = Book.objects.filter(holder=pk)
    query = request.GET.get('q')
    if query:
        user_books = user_books.filter(
            Q(title__icontains=query)|
            Q(author__icontains=query)|
            Q(call_id__icontains=query)
        )
    paginator = Paginator(user_books, 12)
    page_var = 'page'
    page = request.GET.get(page_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)

    book_pk = request.POST.get('book_pk')
    checkin_all = request.POST.get('all')
    if book_pk:
        book = Book.objects.get(id=book_pk)
        user.books_out = user.books_out - 1
        book.available = True
        book.due_date = None
        book.days_to_be_out = 0
        book.holder = None
        user.save()
        book.save()
        return redirect('checkin-user', pk=pk)
    if checkin_all:
        for book in user_books:
            # book = Book.objects.get(id=book.id)
            user.books_out = user.books_out - 1
            book.available = True
            book.due_date = None
            book.days_to_be_out = 0
            book.holder = None
            user.save()
            book.save()
        return redirect('checkin-user-search')
    return render(request, 'CheckinByUser.html', {'user': user, 'books': queryset, 'page_var': page_var, 'Checkin': 'active'})
