from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('expenses/', views.index, name="expenses"),
    path('add-expenses/', views.add_expenses, name="add-expenses"),
    path('edit-expenses/<int:id>/', views.expense_edit, name="edit-expenses"),
    path('delete-expenses/<int:id>/', views.expense_delete, name="delete-expenses"),
    path('search-expenses/', views.search_expenses, name="search-expenses"),
]