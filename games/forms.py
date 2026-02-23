from django import forms

class GameSearchForm(forms.Form):
    query = forms.CharField(label="Game Title", max_length=100)