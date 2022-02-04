from django.urls import path
from . import views

app_name="pdfr"
urlpatterns =[
    path("index/",views.index)
]