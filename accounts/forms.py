from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Save profile with uploaded image
            image = self.cleaned_data.get('image')
            Profile.objects.create(
                user=user,
                image=image if image else 'profile_pics/default.jpg'
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    email = forms.EmailField(required=True)  # now require email
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
        Validate that the username and email match.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if username and email:
            try:
                user = User.objects.get(username=username)
                if user.email.lower() != email.lower():
                    raise forms.ValidationError("Email does not match the username.")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid username or email.")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
