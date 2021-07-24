from django import forms

class signupForm(forms.Form):
    email= forms.CharField(label ='Email')
    password= forms.CharField( label ='Password',min_length=8, widget=forms.PasswordInput)
    confirm_password= forms.CharField(label='Confirm Password',min_length=8, widget=forms.PasswordInput)
    name= forms.CharField(label='Name')
    address= forms.CharField(label='Address')
    phone_number= forms.CharField(label='Phone Number')
class loginForm(forms.Form):
    email= forms.CharField(label='Email')
    password= forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
    