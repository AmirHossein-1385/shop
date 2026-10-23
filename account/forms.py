from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShopUser, WalletTransaction


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ['phone','password','first_name', 'last_name','is_active','is_staff']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone number already exists.')
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Phone number already exists.')

        if not phone.isdigit():
            raise forms.ValidationError('The entered phone number must be a number.')
        if not phone.startswith('09'):
            raise forms.ValidationError('he phone number must start with 09.')
        if len(phone) != 11:
            raise forms.ValidationError('You must enter an 11-digit phone number.')
        return phone

class ShopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ['phone', 'password','first_name', 'last_name','is_active','is_staff']


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone number already exists.')
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Phone number already exists.')

        if not phone.isdigit():
            raise forms.ValidationError('The entered phone number must be a number.')
        if not phone.startswith('09'):
            raise forms.ValidationError('he phone number must start with 09.')
        if len(phone) != 11:
            raise forms.ValidationError('You must enter an 11-digit phone number.')
        return phone


class Register(forms.ModelForm):
        phone = forms.CharField(max_length=100)
        password1 = forms.CharField(max_length=100,label='Password', widget=forms.PasswordInput)
        password2 = forms.CharField(max_length=100,label='repeat password',widget=forms.PasswordInput)
        class Meta:
            model = ShopUser
            fields = ['first_name','last_name']

        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match.')
            return cleaned_data

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('The phone number already exists.')

            if not phone.isdigit():
                raise forms.ValidationError('The entered phone number must be a number.')

            if len(phone) != 11:
                raise forms.ValidationError('You must enter an 11-digit phone number.')

            if not phone.startswith('09'):
                raise forms.ValidationError('he phone number must start with 09.')
            return phone


class ChangePassword(forms.Form):
    new_password = forms.CharField(max_length=100,label='Password', widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=100,label='Repeat Password', widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        repeat_password = cleaned_data.get('repeat_password')
        if new_password != repeat_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class WalletRecharge(forms.ModelForm):
    class Meta:
        model = WalletTransaction
        fields = ['amount']

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('مبلغ وارد شده نامعتبر است.')
        return cleaned_data
