from django import forms
from django.forms.fields import ImageField

class InputLeadForm(forms.Form):
    input_path = forms.URLField(required=True,widget=forms.URLInput(attrs={
        'class' : 'form-control form-control-lg',
        'placeholder' : 'https://www.somesite.com/having-long-address'
    }))
    
class CustomSlugInput(forms.Form):
    slug_input = forms.SlugField(required=True,min_length=5,max_length=20,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder'  : 'your-title',

    }))
class ImageInputForm(forms.Form):
    image_data = forms.ImageField(widget=forms.FileInput(attrs={
        'class' : 'form-control',
    }))