from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'bio', 'location',)
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.cleaned_data.get('profile_picture'):
            profile.profile_picture = self.cleaned_data['profile_picture']
            if commit:
                profile.save()
        return profile