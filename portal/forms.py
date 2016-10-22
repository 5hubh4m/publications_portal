from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search',
        help_text='Enter the search query here.',
        min_length=1
    )