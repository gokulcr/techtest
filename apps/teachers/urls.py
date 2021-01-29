from django.urls import path
from . import views

urlpatterns = [
    path('cv/',views.add_csv, name="cv_add"),
    path('',views.UserHome.as_view(), name="user_home"),
    path('detail_teacher/<int:id>',views.detail_view, name="detail_user"),
    path('detail_teacher',views.detail_view, name="detail_user"),
    path('load_images',views.load_images_from_folder, name="load_data"),
]