from django import forms
from .models import Farm, Cow, MilkingSession, BreedingRecord, CalvingRecord, ProductService


class FarmSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'slogan', 'description', 'phone_number', 'email']



class CowForm(forms.ModelForm):
    class Meta:
        model = Cow
        fields = ['name_or_tag', 'breed', 'date_of_birth', 'gender']


class MilkingSessionForm(forms.ModelForm):
    class Meta:
        model = MilkingSession
        fields = '__all__'

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
