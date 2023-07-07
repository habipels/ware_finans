
from django import forms
from django.forms import ModelForm
from users.models import firma
class firma_ekle(ModelForm):
    tanitici_isim = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style' ,'placeholder': 'Firma Tanıtıcı İsmi'}),help_text='Firma Tanıtıcı İsmi')
    firma_unvani = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style','placeholder': 'Firma Unvanı (Adı)'}),help_text='Firma Unvanı (Adı)')
    Firma_unvani2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-style','placeholder': 'Firma Unvanı (Soyadı)'}),help_text='Firma Unvanı (Soyadı)')
    class Meta:
        model = firma
        fields = [
            "tanitici_isim","firma_unvani","Firma_unvani2"

        ]
