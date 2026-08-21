from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name','message']
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (optional)'}),
             'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your feedback'}),
        }
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False  # make name optional