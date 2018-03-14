from django.db import models
from datetime import datetime, date, timedelta
from random import randint
from django.core.validators import MinValueValidator

# Create your models here.
class Book(models.Model):
    class Meta:
        verbose_name_plural = 'Books'

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1000)])
    price = models.CharField(max_length=6)
    holder = models.ForeignKey('Person', related_name='book_holder', on_delete=models.PROTECT, null=True, blank=True)
    available = models.BooleanField(default=True, blank=True)
    checking_out = models.BooleanField(default=False, blank=True)
    days_to_be_out = models.PositiveSmallIntegerField(default=0, blank=True)
    due_date = models.PositiveSmallIntegerField(null=True, blank=True)
    call_id = models.CharField(max_length=10, editable=False, blank=True)
    r = models.CharField(max_length=4, editable=False, blank=True)
    g = models.CharField(max_length=4, editable=False, blank=True)
    b = models.CharField(max_length=4, editable=False, blank=True)

    """ WIll add the call_id, r, g, and b fields automatically to the database. Call_id is built from
    the first letter of the authors name, first letter of the book title, last 2 digits of the current year,
    seconds of when added since midnight, and the current day # of the year. This method ensures book call_id
    does not repeat for any two books. RGB color code is randomly created as well which is to be used as a cover
    holder for the book.
    """
    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        title = self.title
        self.title = ' '.join(word[0].upper() + word[1:] for word in title.split())
        name = self.author
        self.author = ' '.join(word[0].upper() + word[1:] for word in name.split())
        # checks to see if it is the first time this row in the db is saved
        if not self.id:
            a_first = self.author[:1].upper()
            t_first = self.title[:1].upper()
            day = datetime.now().strftime('%j')
            year = str(date.today().year)[-2:]
            time = str(datetime.now().time())
            time = str((int(time[:2]) * 60 * 60) + (int(time[3:5]) * 60) + int(time[6:8])).zfill(5)
            book_id = (a_first + t_first + year + time + day)
            self.r = randint(10, 255)
            self.g = randint(10, 255)
            self.b = randint(10, 255)
            self.call_id = book_id
        # will add a due date
        elif self.id and self.checking_out:
            today = datetime.today()
            end = str(today + timedelta(days=self.days_to_be_out))
            end = int(end[:4] + end[5:7] + end[8:10])
            self.due_date = end
            self.available = False
            # changes back to not checking out so it does not interfere with updating info
            self.checking_out = False
        # super method is called to save
        super(Book, self).save()

    def __str__(self):
        return '%s' % (self.title + " " + self.call_id)


class Person(models.Model):
    class Meta:
        verbose_name_plural = 'People'

    choices = (
        ('Student', 'Student'),
        ('Staff', 'Staff')
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=90, blank=True, null=True)
    status = models.CharField(max_length=10, choices=choices)
    books_allowed = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    id_number = models.CharField(max_length=10, unique=True)
    books_out = models.PositiveSmallIntegerField(default=0, blank=True)
    day_limit = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return '%s' % (self.first_name + " " + self.last_name + " " + self.id_number)

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        self.first_name = ' '.join(word[0].upper() + word[1:] for word in self.first_name.split())
        self.last_name = ' '.join(word[0].upper() + word[1:] for word in self.last_name.split())
        self.full_name = self.first_name + " " + self.last_name
        super(Person, self).save()

