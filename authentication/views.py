from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from .models import User, Profile
from subscription.models import Subscription
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic import View
from django.views import generic

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db.models import Q


def register_page(request):
    if request.method == "POST":
        usernameField = request.POST.get("username", None)
        emailField = request.POST.get("email", None)
        fullNameField = request.POST.get("fullName", None)
        passwordField = request.POST.get("password", None)
        user = User(
            email=emailField,
            username=usernameField,
            fullName=fullNameField,
            password=make_password(passwordField),
        )
        user.save()
        print("siz yaratildingiz")
    return render(request, "register.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            login_username = request.POST.get("login", None)
            password = request.POST.get("password", None)
            user = authenticate(request, username=login_username, password=password)
            user_2 = User.objects.get(
                Q(username=login_username) | Q(email=login_username)
            )
            if user is not None:
                if user_2.step_completed:
                    login(request, user)
                else:
                    login(request, user)
                    return redirect("/authentication/step")
                return redirect("/")

        return render(request, "login.html")


def forget_password_page(request):
    return render(request, "forget_password.html")


class StepView(View):

    @method_decorator(login_required(login_url="/authentication/login"))
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/authentication/login")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "step.html")

    def post(self, request, *args, **kwargs):
        category = request.POST.get("category", None)
        if category is not None:
            user = request.user
            user.category = category
            user.save()
            return redirect("/authentication/step_second/")


class StepView(View):

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/authentication/login/")
        return render(request, "step_second.html")

    def post(self, request, *args, **kwargs):
        category_2 = request.POST.get("category_2", None)
        if category_2 is not None:
            if category_2 == "Creator":
                request.user.is_creator = True
            elif category_2 == "Business":
                request.user.is_salesman = True
            request.user.save()
            return redirect("/authentication/step_third/")


class ThirdStepView(View):

    def get(self, request, *args, **kwargs):
        is_completed = request.GET.get("third_step_complete")
        if is_completed:
            request.user.step_completed = True
            request.user.save()
            return redirect("/")
        return render(request, "step_third.html")


def help_Center_page(request):
    return render(request, "help.html")


class Profile_page(DetailView):
    model = User
    template_name = "user_profile.html"
    context_object_name = "user"

    def get_object(self, querset=None):
        """
        Bir Userni qanday va uning qaysi fieldni orqali olish uchun ishlatiladi
        """
        kwarg = self.kwargs.get("username", None)
        if kwarg is not None:
            try:
                user = User.objects.get(username=kwarg)
                return user
            except User.DoesNotExist:
                return "None"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwarg = self.kwargs.get("username", None)
        user = User.objects.get(username=kwarg)
        if not user == self.request.user:
            try:
                context['dost'] = Subscription.objects.get(
                    Q(user=user, to=self.request.user) | Q(user=self.request.user, to=user)
                )
            except Subscription.DoesNotExist:
                pass
        return context


class profileUpdateView(UpdateView):
    model = Profile
    fields = ["bio", "avatar", "website", "gender"]
    template_name = "profilUpdate.html"
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        # html orqali kelayotgan malumotni olamiz
        bio = self.request.POST.get("bio")
        avatar = self.request.FILES.get("avatar")
        website = self.request.POST.get("website")
        gender = self.request.POST.get("gender")
        profile = Profile.objects.get(id=self.kwargs.get("pk"))

        if bio:
            profile.bio = bio
        if avatar:
            profile.avatar = avatar
        if website:
            profile.website = website
        if gender:
            profile.gender = gender
        profile.save()  # malumotni saqlab qo'yamiz

        return redirect("update_profile", pk=self.kwargs.get("pk"))


def request_friend(request, id):
    men = request.user
    dost = User.objects.get(id=id)
    
    try:
        s = Subscription.objects.get(
            Q(user=men, to=dost) |
            Q(user=dost, to=men)
        )
    except Subscription.DoesNotExist:
        Subscription.objects.create(user=men, to=dost)
    return redirect(f"/authentication/user_profile/{dost.username}/")


class Notification(TemplateView):
    template_name = "notification.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['request'] = Subscription.objects.filter(
                Q(to=self.request.user)
            )
        except Subscription.DoesNotExist:
            pass
        return context
    
def accept_friend(request, id, friend_request_id):
    user = User.objects.get(id=id)
    try:
        request_friend = Subscription.objects.get(id=friend_request_id)
        if user.id == request_friend.user.id:
            request_friend.accept = True
            request_friend.state = False
            request_friend.save()
    except Subscription.DoesNotExist:
        pass
    return redirect("/authentication/notifications/")
    

# pending

# 7mlrd -- 100%
# mashxurlar -- 0.002
# 60% -- dunyoni qurgan


