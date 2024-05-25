from django import forms
from .models import *


class TicketForm(forms.Form):
    # چون توی تمپلیت وارد کردیم اینجا دیگه بی معنیه و میتوانیم وارد نکنیم و در سابچکت بجای چوز فیلد باید از چر فیلد استفاده کنیم  و پرانتز روبروش رو خالی کنیم
    # SUBJECT_CHOICES = (
    #     ('پیشنهاد', 'پیشنهاد'),
    #     ('انتقاد', 'انتقاد'),
    #     ('گزارش', 'گزارش'),
    # )

    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250 ,required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11,required=True)
    subject = forms.CharField()#choices=SUBJECT_CHOICES

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.startswith('09') or len(phone) != 11:
            raise forms.ValidationError("Phone number must be 11 digits and start with  09")
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("The number is invalid")
            else:
                return phone

class Commentform(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name)< 3: 
                raise forms.ValidationError("name is yoo short")
            else:
                return name
    class Meta:
        model = Comment
        fields = ['name' , 'body']

class CraetePostForm(forms.ModelForm):
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ['title', 'description', 'readingtime', 'category']


class SearchForm(forms.Form):
    query=forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)
    

class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(max_length=20, widget=forms.PasswordInput, label='password')
    password2=forms.CharField(max_length=20, widget=forms.PasswordInput, label='repeat password')

    class Meta:
        model=User
        fields=['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords doesnt match')
        return cd['password2']
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','email']

class AccountEditForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['date_of_birth','bio' ,'job' ,'photo']