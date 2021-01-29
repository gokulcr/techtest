from django.urls import path
from . import views

urlpatterns = [
    path('',views.Loginview.as_view(), name="Renders Login Page"),
    path('signup',views.signup,name="signup"),
]