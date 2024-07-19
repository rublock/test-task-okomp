from django import forms
from mainapp.models import City  # Замените ".models" на ваше приложение


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Введите название города'
