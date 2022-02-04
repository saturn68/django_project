from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages


def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("upass")
        co = request.POST.get("comment")
        pi = request.FILES.get("pic")
        if pw:
            u.set_password(pw)
        if pi:
            u.pic.delete()
            u.pic = pi
        u.comment = co
        u.save()
        login(request, u)
        return redirect("acc:profile")
    return render(request, "acc/update.html")

def delete(request):
    if check_password(request.POST.get("passcheck"), request.user.password):
        request.user.pic.delete()
        request.user.delete()
    return redirect("acc:index")

def profile(request):
    return render(request, "acc/profile.html")

# Create your views here.
def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        ag = request.POST.get("uage")
        co = request.POST.get("comm")
        pi = request.FILES.get("upic")
        User.objects.create_user(username=un, password=pw, age=ag, comment=co, pic=pi)
        return redirect("acc:login")

    return render(request, "acc/signup.html")

def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request,"LOGIN SUCCESS")
            return redirect("acc:index")
        else: # 로그인 실패했어요~~ (19일차에 할거)
            messages.error(request,"아이디와 패스워드 불일치")
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect("acc:index")