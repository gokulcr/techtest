from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View 

from apps.core.forms import FormLogin, UserMasterForm, UserDetailForm
from apps.core.models import Account, AccountDetail


class Loginview(View):

    def get(self, request):
      form_login = FormLogin()
      return render(request, 'loginpage.html', {
          "form_login": form_login
          })

    def post(self,request):
       form_data = FormLogin(request.POST)
       if form_data.is_valid():
            username = form_data.cleaned_data.get('username')
            password = form_data.cleaned_data.get('password') 
            try:
                user = authenticate(email=username, password=password)
            except Exception as e:
                return HttpResponse(e)
            if user == None:
                messages.error(request, 
                    'Incorrect Username or Password')
                return self.get(request)
            else:
                request.session['IS_SUPER_USER'] = user.is_superuser
                request.session['USER_ID'] = user.id
                request.session['USER_NAME'] = user.email
                return redirect("user_home")


def signup(request):
    form_user_master = UserMasterForm(request.POST or None)
    form_user_detail = UserDetailForm(request.POST or None)
    if form_user_master.is_valid() and form_user_detail.is_valid():
        account_obj = form_user_master.save(commit=False)
        account_obj.is_active = True
        account_obj.set_password(form_user_master.cleaned_data.get('password'))
        account_obj.save()
        account_detail_obj = form_user_detail.save(commit=False)
        account_detail_obj.account = account_obj
        account_detail_obj.save()
        messages.success(request, 'Please login to the system')
        return redirect('Renders Login Page')
    return render(request, 'add_user.html', {
        "form_user_master":form_user_master,
        "form_user_detail":form_user_detail
        })
