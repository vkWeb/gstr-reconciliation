from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name = "index"),

    # API Routes
    path("process/",views.process,name = "process"),
]