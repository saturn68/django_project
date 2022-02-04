from django.shortcuts import render,redirect
from book.models import Book
from django.utils import timezone
# Create your views here.
def index(request):
    b=request.user.user.all().order_by('-pubdate')
    
    context={
        "blist":b
    }
    return render(request,"book/index.html",context)

def create(request):
    if request.method =="POST":
        im=request.POST.get("impo")
        sn=request.POST.get("s_name")
        su=request.POST.get("s_url")
        sc=request.POST.get("s_con")
        if sn and su and sc:

            if im:
                imp=True
            else:
                imp=False
            Book(site_name=sn,site_url=su,content=sc,user=request.user,pubdate=timezone.now(),impo=imp).save()
            return redirect("book:index")
    return render(request,"book/create.html")