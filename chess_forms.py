from django import forms

class StartTourForm(forms.Form):
    rows = forms.CharField()
    columns = forms.CharField()
    starting_row = forms.CharField()
    starting_column = forms.CharField()
    
    #username=forms.EmailField()
    #password=forms.CharField(widget=forms.PasswordInput())