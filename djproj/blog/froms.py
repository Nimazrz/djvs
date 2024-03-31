from django import forms


class TicketForm(forms.Form):
    # چون توی تمپلیت وارد کردیم اینجا دیگه بی معنیه و میتوانیم وارد نکنیم
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )

    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250 ,required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11,required=True)
    subject = forms.CharField(choices=SUBJECT_CHOICES)