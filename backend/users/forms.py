from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import CharField
from ckeditor.widgets import CKEditorWidget
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-style', 'placeholder': 'ornek@example.com'}),help_text='Geçerli bir e-posta adresi lütfen.', required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style', 'placeholder': 'Adınız'}),help_text='Adınızı Giriniz', required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style', 'placeholder': 'Soyadınız'}),help_text='Soyadınızı Giriniz', required=True)
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style',"type":"password" ,'placeholder': 'Parolanız'}),help_text='Parolanız', required=True)
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style',"type":"password" ,'placeholder': 'Parolanız Tekrar'}),help_text='Parolanız Tekrar', required=True)
    class Meta:

        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style', 'placeholder': ' Email'}),
        label="Email")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-style', 'placeholder': 'Parola'}))