from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')


def sign_up(request):
    return render(request, 'signup.html')


def login_in(request):
    return render(request, 'login.html')