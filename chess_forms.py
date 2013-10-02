from django import forms

size_choices = (("4","4"), ("5","5"), ("6","6"), ("7","7"), ("8","8"), ("9","9"), ("10","10"), ("11","11"), ("12","12"))
start_choices = (("1","1"),("2","2"),("3","3"),("4","4"), ("5","5"), ("6","6"), ("7","7"), ("8","8"), ("9","9"), ("10","10"), ("11","11"), ("12","12"))

class StartTourForm(forms.Form):
    rows = forms.ChoiceField(choices=size_choices, initial="8")
    columns = forms.ChoiceField(choices=size_choices, initial="8")
    starting_row = forms.ChoiceField(choices=start_choices, initial="1")
    starting_column = forms.ChoiceField(choices=start_choices, initial="1")
    tour_type = forms.ChoiceField(widget=forms.RadioSelect, choices=((False,"Open"), (True,"Closed")))
    
    #username=forms.EmailField()
    #password=forms.CharField(widget=forms.PasswordInput())
    
#for fields that don't require django validation like email and password, maybe just hard code html inputs?

    
