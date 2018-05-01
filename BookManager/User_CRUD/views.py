from django.shortcuts import render
from Database.models import Book, Person
from Database.forms import CreateUser
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
# Code follows the same flow as found in Book_CRUD.views.
# For comments on the code, go to views.py in Book_CRUD
def user_search(request):
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
        "UserSearch": 'active',
        "list": queryset,
        "page_var": page_var
    }
    return render(request, 'active_template/user_search.html', context)

def new_person(request):
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            person = form.save()
            form = CreateUser()
            return render(request, 'active_template/new_person.html', {'form': form,
                                                        'success': "User added successfully."})
    else:
        form = CreateUser()
    return render(request, 'active_template/new_person.html', {'form': form})

def edit_user(request, pk):
    user = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        form = CreateUser(request.POST, instance=user)
        if form.is_valid():
            person = form.save()
            return redirect('userinfo', pk=user.pk)
    else:
        form = CreateUser(instance=user)
    return render(request, 'active_template/edit_user.html', {'form': form})

def user_info(request, pk):
    person = get_object_or_404(Person, pk=pk)
    book = Book.objects.filter(holder=pk)
    return render(request, 'active_template/user-info.html', {'user': person, 'books': book})

def delete_user(request, pk):
    user = Person.objects.get(pk=pk)
    user.delete()
    return redirect('users')