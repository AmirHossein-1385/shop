from django import forms
from account.models import ShopUser
from orders.models import Order


class VerifyPhoneForm(forms.Form):
    phone = forms.CharField(label='Phone Number',max_length=11)

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('The phone number already exists.')

        if not phone.isdigit():
            raise forms.ValidationError('Phone Number must be an integer')

        if not phone.startswith('09'):
            raise forms.ValidationError('The phone number must start with 09')

        if len(phone) != 11:
            raise forms.ValidationError('The phone number must have 11 digits')

        return phone


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','address','postal_code','city','province']

