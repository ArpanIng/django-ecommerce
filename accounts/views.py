from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import RegistrationModelForm
from .models import Account


def register_view(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        form = RegistrationModelForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            usernmae = email.split("@")[0]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=usernmae,
                password=password,
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request, message="Account created successfully!")
            return redirect("accounts:login")
    else:
        form = RegistrationModelForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, message="Invalid email or password")
    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect("accounts:login")
