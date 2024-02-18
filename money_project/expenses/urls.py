from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("expenses/", views.index, name="index"),
    path("add-expenses/", views.add_expenses, name = "add-expenses")
]