from django.shortcuts import render
from userpreferences.models import Currencies, UserPreferences
from django.contrib import messages

# Create your views here.


def index(request):
    context = {}
    if request.method == "GET":
        currency_data = []
        currencies_queryset = Currencies.objects.all()
        for obj in currencies_queryset:
            currency_data.append({"name": obj.name, "alias":obj.alias})
        context["currencies"] = currency_data
        user = request.user
        if UserPreferences.objects.filter(user=user).exists():
            context["selected"] = UserPreferences.objects.filter(user=user).first().currency
        else:
            context["selected"] = "Choose.."
        return render(request, 'preferences/index.html', context)
    else:
        preference, _ = UserPreferences.objects.get_or_create(user=request.user)
        value = request.POST.get("currency")
        if value:
            preference.currency = value
            context["selected"] = value
        preference.save()
        messages.success(request, "Changes Saved!")
        return render(request, 'preferences/index.html', context)

    