from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']


from django import forms

class AudioForm(forms.Form):
    file = forms.FileField()


class ImageUploadForm(forms.Form):
    image = forms.ImageField()



