from django import forms

class UploadCodeForm(forms.Form):
    file = forms.FileField()


