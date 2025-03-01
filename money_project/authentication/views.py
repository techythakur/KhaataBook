from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.validators import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
import threading
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import tokenGenerator
from django.contrib.auth import authenticate, login, logout


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently=False)

class LoginView(View):

    def get(self, request):
        return render(request, 'authentication/login.html')

class RegistrationView(View):

    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        context = {
            "fieldValues" : request.POST
        }

        if not User.objects.filter(username=username, email=email).exists():
            if len(password)<6:
                messages.error(request, "Password too short!")
                return render(request, 'authentication/register.html', context)
            
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_active=False
            user.save()
            messages.success(request, "Account Successfully Created!")

            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': tokenGenerator.make_token(user)})

            activate_url = "http://"+domain+link

            email_subject = "Account Created | please Activate your Account"
            email_body = f"Hello {user.username}, \n" + \
            "To verify your account, Please go to this link: " + activate_url
            email_ids = [email]

            email = EmailMessage(
                email_subject,
                email_body,
                "from@example.com",
                email_ids,
            )

            EmailThread(email).start()
            # email.send(fail_silently=False)

            # return render(request, 'authentication/register.html')
            return redirect("login")
        
        messages.error(request, "Account Already Exists!")

        return render(request, 'authentication/register.html', context)

class UserValidationView(View):

    def post(self, request):
        context = {
            "flag": False,
            "msg": ""
        }
        username = request.POST.get("username")
        if not username or not username.isalnum():
            context["msg"] = "Username should only contain alphanumeric characters"
            return JsonResponse(context)
        
        if User.objects.filter(username=username).exists():
            context["msg"] = "Username already exists!"
            return JsonResponse(context)

        context["flag"] = True
        context["msg"] = "Valid Username"
        return JsonResponse(context)

class EmailValidationView(View):
    
    def post(self, request):
        context = {
            "flag": False,
            "msg": ""
        }
        email = request.POST.get("email")

        try:
            validate_email(email)
        except Exception:
            context["msg"] = "Invalid Email!"
            return JsonResponse(context)
        
        if User.objects.filter(email=email).exists():
            context["msg"] = "Email already exists!"
            return JsonResponse(context)

        context["flag"] = True
        context["msg"] = "Valid email!"
        return JsonResponse(context)

class VerificationView(View):

    def get(self, request, uidb64, token):
         
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(id))

            if not tokenGenerator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            
            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, "Account Activated Successfully!")

        except Exception: ...


        return redirect('login')


class LoginView(View):

    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    welcome_message = "Welcome, "+ user.get_username()
                    messages.success(request, welcome_message + " You have logged in Successfully")
                    return redirect('/expenses/')

                messages.error(request,"Your account is not active, please check your email")
                return render(request, 'authentication/login.html')

            messages.error(request,"Invalid Credentials!")
            return render(request, 'authentication/login.html')

        messages.error(request,"please fill all fields")
        return render(request, 'authentication/login.html')
        

class LogoutView(View):

    def get(self, request):
        return redirect('login')

    def post(self, request):
        logout(request)
        messages.success(request, "You have been Logged Out Successfully!")
        return redirect('login')
