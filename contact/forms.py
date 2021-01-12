from django import forms

class ContactForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


