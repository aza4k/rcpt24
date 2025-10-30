from django import forms
from django.contrib.auth.models import User
from .models import Pharmacy

class PharmacyRegisterForm(forms.ModelForm):
    username = forms.CharField(label="Foydalanuvchi nomi", max_length=100)
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Parolni tasdiqlang", widget=forms.PasswordInput)

    class Meta:
        model = Pharmacy
        fields = ['name', 'address', 'phone', 'working_hours']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos emas!")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        pharmacy = super().save(commit=False)
        pharmacy.user = user
        if commit:
            pharmacy.save()
        return pharmacy
