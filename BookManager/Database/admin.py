from django.contrib import admin
from .models import Person, Book

# Register your models here
admin.site.register(Person)
admin.site.register(Book)