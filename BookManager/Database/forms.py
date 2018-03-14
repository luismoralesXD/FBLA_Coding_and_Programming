from django import forms
from .models import Book, Person

class Createbook(forms.ModelForm):    
    class Meta:
        model= Book
        fields= ['title',
                 'author',
                 'year',
                 'price']
    
    def __init__(self, *args, **kwargs):
        super(Createbook, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'title-field input',
            'placeholder': 'Book Title'})
        self.fields['author'].widget.attrs.update({
            'class': 'author-field input',
            'placeholder': 'Author'})
        self.fields['year'].widget.attrs.update({
            'class': 'year-field input',
            'placeholder': 'Year Published'})
        self.fields['price'].widget.attrs.update({
            'class': 'price-field input',
            'placeholder': 'Book Value(Ex: 37.56, 34.00)'})

class CreateUser(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'status', 'books_allowed', 'id_number', 'day_limit']

    def __init__(self, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Last Name'})
        self.fields['status'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Student'})
        self.fields['books_allowed'].widget.attrs.update({
            'class': 'input',
            'placeholder': '# of books allowed'})
        self.fields['id_number'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Id Number'})
        self.fields['day_limit'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Days given to checkout book'})