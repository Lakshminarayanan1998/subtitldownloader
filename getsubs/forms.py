from django import forms


class MovieForm(forms.Form):
        movie_name= forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}),label="")
        fields=['movie_name']
