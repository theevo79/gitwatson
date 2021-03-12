from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm

# Create your views here.
def register(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			form.save()
            
		return redirect("users:login")
	else:
		form = RegisterForm()

	return render(response, "users/register.html", {"form":form})

def index(request):
	#if not request.user.is_authenticated:
	#	return HttpResponseRedirect(reverse("users:login"))
	return render(request, "users/base.html")

def login_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("news:index1"))
		else:
			return render(request, "users/login.html", {
				"message": "Invalid credentials"
				})

	return render(request, "users/login.html")

def logout_view(request):
	logout(request)
	return render(request, "users/login.html", {
		"message": "Logged out."
		})

