from django.shortcuts import redirect, render
from .models import Board, Reply
from acc.models import User
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def index(request):
    kw = request.GET.get("kw", "")
    cate = request.GET.get("cate", "")
    pg = request.GET.get("page", 1)

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b=Board.objects.none()
            
        elif cate=="con":
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()

    
    pag = Paginator(b,5)
    obj = pag.get_page(pg)
    context = {
        "blist" : obj,
        "cate":cate,
        "kw":kw
    }
    return render(request, "board/index.html", context)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else: # 19일차 에러메세지 띄울 예정!
        messages.warning(request,"작성자가 아닙니다")
    return redirect("board:detail", bpk)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)


def update(request, bpk):
    b = Board.objects.get(id=bpk)
    
    # 다른사람이 악의적으로 접근했을 때 (19일차)
    if request.user != b.writer:
        messages.warning(request,"삭제권한 없음")
        return redirect("board:index")

    if request.method == "POST":
        b.subject = request.POST.get("sub")
        b.content = request.POST.get("con")
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b":b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user, content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:
        messages.error(request,"삭제권한이 없습니다") # 19일차 메세지 띄워줌!!
    return redirect("board:index")

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b":b,
        "rlist":r,
    }
    return render(request, "board/detail.html",context)

def likey(request,bpk):
    
    b=Board.objects.get(id=bpk)
    
    b.likey.add(request.user)
    return redirect('board:detail',bpk)
    
def unlikey(request,bpk):
    b=Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect('board:detail',bpk)
    