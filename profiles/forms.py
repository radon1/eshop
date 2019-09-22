from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    '''Форма профиля'''

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'city',
            'company_name',
            'address',
            'postcode',
            'phone',
            'country',
            'state'
        )