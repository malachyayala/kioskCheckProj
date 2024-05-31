from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import bleach
from .models import KioskCheck


class KioskCheckForm(forms.ModelForm):

    class Meta:
        PRINTER_CHOICES = [
            ('', '--Please choose an option--'),
            ('wcc-bf-lab-bw-1', 'WCC-BF-LAB-BW-1'),
            ('wcc-bf-lab-c-1', 'WCC-BF-LAB-COLOR-1'),
            ('wcc-2f-bw-1', 'WCC-2F-SOR-BW-1'),
            ('wcc-2f-c-1', 'WCC-2F-SOR-COLOR-1'),
            ('wcc-1f-hrk-bw-1', 'WCC-1F-HRK-BW-1'),
            ('wcc-1f-hrk-bw-2', 'WCC-2F-HRK-BW-2'),
            ('lan-2f-lob-bw-2', 'LAN-2F-LOB-BW-2'),
            ('lan-2f-lob-c-1', 'LAN-2F-LOB-COLOR-1'),
            ('lan-2f-221-bw-1', 'LAN-2F-221-BW-1'),
            ('lan-3f-352-bw-1', 'LAN-3F-352-BW-1'),
            ('lan-3f-353-bw-1', 'LAN-3F-353-BW-1'),
        ]

        PRINTER_STATUS_CHOICES = [
            ('', '--Please choose an option--'),
            ('good', 'Good'),
            ('misfeed', 'Paper misfeed'),
            ('call-service', 'Call service'),
            ('toner', 'Toner depleted'),
        ]

        TONER_STATUS_CHOICES = [
            ('', '--Please choose an option--'),
            ('full', 'Full'),
            ('low', 'Low'),
            ('empty', 'Empty'),
        ]

        model = KioskCheck
        exclude = ['user']
        fields = [
            'printer', 'reams_used', 'issues', 'toner_status',
            'issue_description', 'ricoh_ticket', 'servicenow_ticket'
        ]
        widgets = {
            'printer': forms.Select(choices=PRINTER_CHOICES, attrs={'class': 'form-control'}),
            'reams_used': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 4}),
            'issues': forms.Select(choices=PRINTER_STATUS_CHOICES, attrs={'class': 'form-control'}),
            'toner_status': forms.Select(choices=TONER_STATUS_CHOICES, attrs={'class': 'form-control'}),
            'issue_description': forms.Textarea(attrs={'class': 'form-control'}),
            'ricoh_ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'servicenow_ticket': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_printer(self):
        data = self.cleaned_data['printer']
        cleaned_data = bleach.clean(data, tags=[])
        return cleaned_data

    def clean_issue_description(self):
        data = self.cleaned_data['issue_description']
        allowed_tags = ['b', 'i', 'u', 'a', 'p']
        cleaned_data = bleach.clean(data, tags=allowed_tags)
        return cleaned_data

    def clean_reams_used(self):
        data = self.cleaned_data['reams_used']
        if not (0 <= data <= 4):
            raise forms.ValidationError('Reams Used must be between 0 and 4.')
        return data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    registration_code = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'registration_code']

    def clean_registration_code(self):
        code = self.cleaned_data.get('registration_code')
        if code != 'HLSITS':
            raise forms.ValidationError('Invalid registration code.')
        return code
