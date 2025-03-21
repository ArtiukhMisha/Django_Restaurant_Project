from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django import views


# Create your views here.
def home(request):
    return render(request, "inventory/home.html")


class LogoutView(views.View):
    next_page = reverse_lazy("home")
    success_url = reverse_lazy("home")

    def get(self, request):
        return render(request, "login_app/logout.html")

    def post(self, request):
        logout(request)
        return render(request, "inventory/home.html")

    def get_success_url(self):
        return reverse_lazy("home")


class LoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("login")
    template_name = "login_app/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "login_app/logged_in.html")
        return super().get(request)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "login_app/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        access_level = form.cleaned_data.get("access_level")
        user = self.object

        if access_level == "kelner":
            group = Group.objects.get(name="Kelner Access")
        elif access_level == "manager":
            group = Group.objects.get(name="Manager Access")

        user.groups.add(group)
        return response
