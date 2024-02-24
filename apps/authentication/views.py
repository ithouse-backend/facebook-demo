from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from .models import User, Friendship
from django.contrib import messages
from .form import *
from django.db import IntegrityError
from django.db.models import Q

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


class CustomPasswordResetView(PasswordResetView):
    """
    Password reset ya'ni parolni o'zgartirish tugmasiga bosganda, shu
    manzilga keladi. Buning vazifasi bizga email kiritish uchun input ochib berish
    va undan so'ng password reset done bo'limiga o'tadi
    """

    email_template_name = "registration/password_reset_email.html"
    template_name = "registration/password_reset_form.html"
    form_class = CustomPasswordResetForm
    success_url = "/password-reset-done/"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Yangi parolni kiritish joyi
    """

    template_name = "registration/password_reset_confirm.html"
    form_class = SetPasswordForm
    success_url = "/password-reset-complete/"


# GET -- login
# POST -- register
def login_page(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            email = request.GET.get("email")
            password = request.GET.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home/")
            else:
                print("error")
            return render(request, "authentication/login.html")
        else:
            return redirect("/home/")

    elif request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        password = request.POST.get("password")

        try:
            user = User.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                birthday=birthday,
                gender=gender,
                password=make_password(password),
            )
            login(request, user)

            return redirect("/")
        except IntegrityError as p:
            if 'unique constraint' in str(p).lower():
                messages.error(request, "Email is already chosen!")
                return redirect('/')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(
            request,
            "You are logged out from our website. Please go to login page to authenticate",
        )
        return redirect("/")


def user_profile(request, user_id):
    # request.user ---------------- joriy foydalanuvchi
    # Q ---> bir nechta malumotni filter qilsak ishlatish shart
    friends = Friendship.objects.filter(
        Q(user1=request.user) |
        Q(user2=request.user)
    ).count()
    user = User.objects.get(unique_id=user_id)
    if request.method == 'POST' and request.user:
        avatar_change = request.FILES.get("profile__change-avatar")
        banner_change = request.FILES.get("profile__change-banner")
        about_update = UpdateAboutForm(
            request.POST, instance=request.user.about)

        if about_update.is_valid():
            about_update.save()
            return redirect("/")
        if avatar_change:
            profile = Profile.objects.get(user=request.user)
            profile.avatar = avatar_change
            profile.save()
        if banner_change:
            profile = Profile.objects.get(user=request.user)
            profile.banner = banner_change
            profile.save()
    else:
        about_update = UpdateAboutForm(instance=request.user)

    context = {
        "about_update": about_update,
        "user": user,
        "friends": friends
    }

    return render(request, "authentication/profile.html", context)
