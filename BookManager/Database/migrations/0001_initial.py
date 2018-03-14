# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1000)])),
                ('price', models.CharField(max_length=6)),
                ('available', models.BooleanField(default=True)),
                ('checking_out', models.BooleanField(default=False)),
                ('days_to_be_out', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('due_date', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('call_id', models.CharField(max_length=10, blank=True, editable=False)),
                ('r', models.CharField(max_length=4, blank=True, editable=False)),
                ('g', models.CharField(max_length=4, blank=True, editable=False)),
                ('b', models.CharField(max_length=4, blank=True, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=50)),
                ('full_name', models.CharField(max_length=90, blank=True, null=True)),
                ('status', models.CharField(max_length=10, choices=[('Student', 'Student'), ('Staff', 'Staff')])),
                ('books_allowed', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('id_number', models.CharField(max_length=10, unique=True)),
                ('books_out', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('day_limit', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name_plural': 'People',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='holder',
            field=models.ForeignKey(blank=True, null=True, related_name='book_holder', on_delete=django.db.models.deletion.PROTECT, to='Database.Person'),
        ),
    ]
