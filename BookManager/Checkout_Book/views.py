from django.shortcuts import render
from Database.models import Book, Person
from Database.forms import Createbook, CreateUser
from datetime import date
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def checkout_book(request):
    user_list = Person.objects.all()
    query = request.GET.get('q')
    if query:
        user_list = user_list.filter(
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)|
            Q(full_name__icontains=query)|
            Q(id_number__icontains=query)
        )
    paginator = Paginator(user_list, 10)
    page_var = 'page'
    page = request.GET.get(page_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "Checkout": "active",
        "list": queryset,
        "page_var": page_var
    }
    return render(request, 'checkout.html', context)

def checkout_to_user(request, pk):
    user = Person.objects.get(pk=pk)
    books = Book.objects.filter(available=True)
    checkout = request.POST.get('book_pk')
    query = request.GET.get("q")
    if query:
        books = books.filter(
            Q(title__icontains=query)|
            Q(author__icontains=query)|
            Q(call_id__icontains=query)
        )
    paginator = Paginator(books, 12)
    page_var = "page"
    page = request.GET.get(page_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    
    if checkout:
        book_chosen = Book.objects.get(pk=checkout)
        user.books_out = user.books_out + 1
        book_chosen.holder = user
        book_chosen.available = False
        book_chosen.checking_out = True
        book_chosen.days_to_be_out = user.day_limit
        user.save()
        book_chosen.save()
        return redirect('checkout-user', pk=pk)

    return render(request, 'checkout_final.html',{'user': user, 'books': queryset})
