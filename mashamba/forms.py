from django import forms
from django.contrib.auth.models import User
from .models import Farm, Cow, MilkingSession, BreedingRecord, CalvingRecord, ProductService


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class FarmSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'slogan']



class CowForm(forms.ModelForm):
    class Meta:
        model = Cow
        fields = ['name_or_tag', 'breed', 'date_of_birth', 'gender']


class MilkingSessionForm(forms.ModelForm):
    class Meta:
        model = MilkingSession
        fields = ['milk_yield', 'milking_time']


    def clean_cow(self):
        cow = self.cleaned_data.get('cow')
        if cow.gender != 'Female':
            raise forms.ValidationError("Milking sessions can only be added for female cows.")
        return cow

class BreedingRecordForm(forms.ModelForm):
    class Meta:
        model = BreedingRecord
        fields = '__all__'

    def clean_cow(self):
        cow = self.cleaned_data.get('cow')
        if cow.gender != 'Female':
            raise forms.ValidationError("Breeding records can only be added for female cows.")
        return cow

class CalvingRecordForm(forms.ModelForm):
    class Meta:
        model = CalvingRecord
        fields = '__all__'

    def clean_cow(self):
        cow = self.cleaned_data.get('cow')
        if cow.gender != 'Female':
            raise forms.ValidationError("Calving records can only be added for female cows.")
        return cow
