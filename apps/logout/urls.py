from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="Clears the session and redirects to login page"),
]