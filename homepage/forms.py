from django import forms

class MovieForm(forms.Form):
    search_movie = forms.CharField(label='Search Movie', max_length=100)