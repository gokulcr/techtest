from django import forms
from django.http import HttpResponse

from apps.core.models import Account, AccountDetail


class FormLogin(forms.Form) :
    username = forms.EmailField( max_length=254, required=True)		
    password = forms.CharField(max_length=20, required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))		
    
    def clean(self):
        data = self.cleaned_data
        username = data["username"]
        password = data["password"]
        if username == None:
            self.add_error("username", "Username is required")
        if password == None:
            self.add_error("password", "Password is required")
        return data

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder':'Email'})
        self.fields['password'].widget.attrs.update({'class':'form-control'})
        self.fields['password'].widget.attrs.update({'placeholder':'Password'})


class UserMasterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(min_length=6, max_length=254, required=True,widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(UserMasterForm, self).__init__(*args, **kwargs)				   
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'placeholder':'Password'})
        try:
            if self.initial['password']:
                self.initial['password'] = ""
        except:
            pass
        try:
            if self.initial['email']!="":
                self.fields['email'].widget.attrs['readonly'] = True
        except Exception as e:
            pass
    
    class Meta:
            model = Account
            fields = ("email","password")
    
    def clean(self):
        cleaned_data = super(UserMasterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class UserDetailForm(forms.ModelForm):
    address = forms.CharField( widget=forms.Textarea(attrs={'width':"50%", 'cols' : "80", 'rows': "2", }),required=False )
    
    def __init__(self, *args, **kwargs):
        super(UserDetailForm, self).__init__(*args, **kwargs)
        self.fields['user_first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['user_last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].label = "Mobile"
        self.fields['address'].widget.attrs.update({'class': 'form-control','widget':'forms.Textarea'})                    #self.fields['Account'].widget.attrs.update({'class': 'form-control'})                             #self.fields['user_last_name'].widget.attrs.update({'class': 'form-control'})	
    
    class Meta:
        model = AccountDetail
        fields = ("user_first_name","user_last_name","phone","address")
