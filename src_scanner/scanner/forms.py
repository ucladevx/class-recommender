import re
from django import forms
# from django.contrib.auth.models import User
from scanner.models import CustomUser as User


from phonenumber_field.formfields import PhoneNumberField

 
CHOICES = (
            ('',''),
            ('sms.alltelwireless.com', 'Alltel'), ('txt.att.net', 'AT&T'), ('sms.myboostmobile.com', 'Boost Mobile'),
            ('text.republicwireless.com', 'Republic Wireless'), ('messaging.sprintpcs.com', 'Sprint'), ('tmomail.net', 'T-Mobile'),
            ('email.uscc.net', 'U.S. Cellular'), ('vtext.com', 'Verizon Wireless'), ('vmobl.com', 'Virgin Mobile'),
        )

    
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label="Username", error_messages={ 'invalid': "This value must contain only letters, numbers and underscores." })
    phone_number = PhoneNumberField(label="Phone Number")
    carrier = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control',}), choices=CHOICES, required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label="Email address")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label="Password (again)")
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            if '@' in self.cleaned_data['username']:
                raise forms.ValidationError("Username cannot contain '@'")
            return self.cleaned_data['username']
        raise forms.ValidationError("Username already exists. Please try another one.")

    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError("Email already exists. Please try another one.")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data

    def clean_carrier(self):
        value = self.cleaned_data['carrier']
        if value == self.fields['carrier'].choices[0][0]:
            raise forms.ValidationError('Must select a carrier')
        return value


class UpdateForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label="Username", error_messages={ 'invalid': "This value must contain only letters, numbers and underscores." })
    phone_number = PhoneNumberField(label="Phone Number")
    carrier = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control',}), choices=CHOICES, required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label="Email address")


    def clean_carrier(self):
        value = self.cleaned_data['carrier']
        if value == self.fields['carrier'].choices[0][0]:
            raise forms.ValidationError('Must select a carrier')
        return value



