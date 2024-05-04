from django import forms
from .models import *
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


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
        fields = ['title', 'description', 'readingtime']

    def clean_writer(self):
        writer=self.cleaned_data['writer']
        user_names = User.objects.all()
        for i in range(0,len(user_names)):
            print(i)
            print(user_names[i].username)
            if writer == user_names[i].username:
                return 4

class SearchForm(forms.Form):
    query=forms.CharField()


