from django.shortcuts import render
from Database.models import Book
from Database.forms import Createbook
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def book_search(request):
    book_list = Book.objects.all()  # sets all books to the book_list var
    query = request.GET.get("q")  # set the search term in the query var
    if query:  # if there is a search term, apply these filters to the books
        book_list = book_list.filter(
            Q(title__icontains=query)|
            Q(author__icontains=query)|
            Q(call_id__icontains=query)
        )
    paginator = Paginator(book_list, 12)  # sets what to paginate and how many per page
    page_var = "page"  # used when multiple pages to get books on x page
    page = request.GET.get(page_var)

    try:  # if a page is passed...
        queryset = paginator.page(page)  # tries to get that page
    except PageNotAnInteger:  # if page is not a number...
        queryset = paginator.page(1)  # returns the first page
    except EmptyPage:  # if page number is empty...
        queryset = paginator.page(paginator.num_pages)  # returns the last page available

    context = {
        'BookSearch': 'active',
        "list": queryset,
        "page_var": page_var,
    }  # pass the data to be used
    return render(request, 'active_template/book_search.html', context)

def create_book(request):
    if request.method == "POST":  # if form is being submitted..
        form = Createbook(request.POST)  
        if form.is_valid():  # checks if the form is valid, all necessary fields filled appropriately
            book = form.save()  # saves the form
            form = Createbook()  # sets a new form to form var and send back to empty page
            return render(request, 'active_template/create_book.html', {'form': form, 'success': "Book created successfully."})
    else:  # if accessing page to add book..
        form = Createbook()  # sends empty form
    return render(request, 'active_template/create_book.html', {'form': form})

def book_info(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'active_template/book-info.html', {'book': book})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":  # if user submits the update form...
        form = Createbook(request.POST, instance=book)
        if form.is_valid():  # check everything is entered correctly 
            book = form.save()  # save the new updated info 
            return redirect('bookinfo', pk=book.pk)  # take user back to book info page
    else:  # if user is going to update book
        form = Createbook(instance=book)  # fill in form with already saved info
    return render(request, 'active_template/edit_book.html', {'form': form})

def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('booksearch')
