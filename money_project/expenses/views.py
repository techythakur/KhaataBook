import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import  messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='login')
def index(request):
    expenses = Expense.objects.all()
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "expenses": expenses,
        "page_obj": page_obj
    }
    return render(request, "expenses/index.html", context)

@login_required(login_url='login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {
            "categories": categories,
            "values": request.POST
        }
    if request.method == "GET":
        return render(request, "expenses/add_expenses.html", context)
    if request.method == "POST":
        amount = request.POST.get("amount")
        if not amount:
            messages.error(request, "Amount is Required!")
            return render(request, "expenses/add_expenses.html", context)
        description = request.POST.get("description")
        if not description:
            messages.error(request, "Description is Required!")
            return render(request, "expenses/add_expenses.html", context)
        date = request.POST.get("expense_date")
        if not date:
            messages.error(request, "Date is Required!")
            return render(request, "expenses/add_expenses.html", context)
        category = request.POST.get("category")

        Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
        messages.success(request, "Expenses Saved Successfully!")

        return redirect("expenses")
    
@login_required(login_url='login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        "expenses": expense,
        "values": expense,
        "categories": categories,
    }
    if request.method == "GET":
        return render(request, "expenses/edit_expenses.html", context)
    if request.method == "POST":
        amount = request.POST.get("amount")
        if not amount:
            messages.error(request, "Amount is Required!")
            return render(request, "expenses/edit_expenses.html", context)
        description = request.POST.get("description")
        if not description:
            messages.error(request, "Description is Required!")
            return render(request, "expenses/edit_expenses.html", context)
        date = request.POST.get("expense_date")
        if not date:
            messages.error(request, "Date is Required!")
            return render(request, "expenses/edit_expenses.html", context)
        category = request.POST.get("category")
        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category
        expense.save()
        messages.success(request, "Expense Updated Successfully!")
        return redirect("expenses")

@login_required(login_url='login')
def expense_delete(request, id):
    try:
        expense = Expense.objects.get(pk=id)
        expense.delete()
        messages.success(request, "Expense removed Successfully!")
    except Exception:
        messages.info(request, "No expense Found!")
    
    return redirect("expenses")

@csrf_exempt
def search_expenses(request):
    if request.method =="POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = Expense.objects.filter(
            Q(amount__icontains=search_str, owner=request.user) | 
            Q(date__icontains=search_str, owner=request.user) | 
            Q(description__icontains=search_str, owner=request.user) | 
            Q(category__icontains=search_str, owner=request.user)
        )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)