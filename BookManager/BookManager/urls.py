"""BookManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Book_CRUD import views as BookViews
from Checkin_Book import views as CheckinViews
from Checkout_Book import views as CheckoutViews
from Database import views as DBViews
from User_CRUD import views as UserViews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', DBViews.home, name="home"),
    url(r'^book/$', BookViews.book_search, name="booksearch"),
    url(r'^book/create/$', BookViews.create_book, name="registerbook"),
    url(r'^book/(?P<pk>\d+)/$', BookViews.book_info, name="bookinfo"),
    url(r'^book/(?P<pk>\d+)/edit/$', BookViews.edit_book, name="editbook"),
    url(r'^book/duetoday/$', DBViews.due_today, name="duetoday"),
    url(r'^book/out/$', DBViews.checkedout_books, name="checked_out"),
    url(r'^book/overdue/$', DBViews.overdue, name="overdue"),
    url(r'^checkin/$', CheckinViews.checkin_books_individually, name="checkin"),
    url(r'^checkin/individual/$', CheckinViews.checkin_by_user, name="checkin-user-search"),
    url(r'^checkin/individual/(?P<pk>\d+)/$', CheckinViews.checkin_user_books, name="checkin-user"),
    url(r'^checkout/$', CheckoutViews.checkout_book, name="checkout"),
    url(r'^checkout/(?P<pk>\d+)/$', CheckoutViews.checkout_to_user, name="checkout-user"),
    url(r'^delete-book/(?P<pk>\d+)/$', BookViews.delete_book, name="delete-book"),
    url(r'^delete-person/(?P<pk>\d+)/$', UserViews.delete_user, name="delete-user"),
    url(r'^help/$', DBViews.help, name="help-page"),
    url(r'^user/$', UserViews.user_search, name="users"),
    url(r'^user/create/$', UserViews.new_person, name="newperson"),
    url(r'^user/(?P<pk>\d+)/$', UserViews.user_info, name="userinfo"),
    url(r'^user/(?P<pk>\d+)/edit/$', UserViews.edit_user, name="edituser"),
]
