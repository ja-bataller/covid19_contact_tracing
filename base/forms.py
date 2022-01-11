from django import forms
from django.forms import ModelForm, fields, widgets
from .models import UserAccount

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('full_name', 'gender', 'contact_number', 'email_address', 'home_address', 'password')
        
        labels = {
                'full_name': (''),
                'gender': (''),
                'contact_number': (''),
                'email_address': (''),
                'home_address': (''),
                'password': (''),
            }

        gender_choices= [
        ('', 'choose your gender here'),
        ('male', 'Male'),
        ('female', 'Female'),
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name', 'autocomplete': 'off'}),
            'gender' : forms.Select(choices=gender_choices, attrs={'class': 'form-select'}),
            'contact_number': forms.TextInput(attrs={'id': 'inputBox','name':'contact_number','placeholder': 'Contact Number', 'autocomplete': 'off', 'onkeydown':"return event.keyCode !== 16 "
            ,'pattern':"[0-9]{11}",'oninvalid':"this.setCustomValidity('Please enter 11 Digit Contact Number (Ex. 09051234567)')"
            ,'oninput':"this.setCustomValidity('')"
            }),
            'email_address': forms.EmailInput(attrs={'placeholder': 'Email Address','name':'email_address','autocomplete': 'off'}),
            'home_address': forms.TextInput(attrs={'placeholder': 'Home Address', 'autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password','name':'password','autocomplete': 'off'}),
            # <input type="text" name="" placeholder="Full Name" />
            # <input type="number"
            #     onkeydown="return event.keyCode !== 69 && event.keyCode !== 190 && event.keyCode !== 187 && event.keyCode !== 189"
            #     name="" placeholder="Mobile Number" />
            # <input type="email" name="" placeholder="Email Address" />
            # <input type="text" name="" placeholder="Home Address" />
            # <input type="password" name="" placeholder="Create Password" />
            # <input type="password" name="" placeholder="Confirm Password" />
            
        }