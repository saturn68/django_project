from django.shortcuts import render
#import googletrans
from googletrans import Translator
import googletrans
# Create your views here.


text1 = "Hello welcome to my website!"
def index(request):
    context={
        "ndict":googletrans.LANGUAGES
    }
    googletrans.LANGUAGES
    if request.method=="POST":
        d={1:"one",2:"two",3:"three",4:"four"}
        bf=request.POST.get("bf")
        src=request.POST.get("src")
        dest=request.POST.get("dest")
        translator=Translator()
        trans1=translator.translate(bf,src=src,dest=dest)
        context.update({
            "af":trans1.text,
            "bf":bf,
            "src":src,
            "dest":dest,
        })



    return render(request,"trans/index.html",context)

