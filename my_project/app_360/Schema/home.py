'''from django import forms

class MyForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    #companyid = forms.IntegerField()
'''

from django import forms

class MyForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())




from django import forms
from app_360.Schema.ParticipantInviteModel import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'designation', 'department', 'location', 'email', 'dob', 'country', 'state']