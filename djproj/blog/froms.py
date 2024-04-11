from django import forms
from .models import Comment

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

    #اعتبار سنجی برای هرمقدار که خودمون بخوایم
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("The number is invalid")
            else:
                return phone
            

class Commentform(forms.ModelForm):
    class  Meta:
        model = Comment
        fields = ['name' , 'body']