from django.urls import path,include
from .views import RegistrationView, UserValidationView, LoginView, VerificationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("validate-username/", csrf_exempt(UserValidationView.as_view()), name="validate-username"),
    path("validate-email/", csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path("activate/<uidb64>/<token>/", VerificationView.as_view(), name="activate"),
]
