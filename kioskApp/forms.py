from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import bleach
from .models import KioskCheck, ChargingStationCheck, PrinterLocation, ChargingStationLocation


class KioskCheckForm(forms.ModelForm):
    printer = forms.ModelChoiceField(queryset = PrinterLocation.objects.all(),
                                     empty_label = "--Please choose an option--",
                                     widget = forms.Select(attrs = {'class': 'form-control'}))

    class Meta:
        PRINTER_STATUS_CHOICES = [
            ('', '--Please choose an option--'),
            ('no_issues', 'No issues found'),
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

        COMPUTER_ISSUE_CHOICES = [
            ('', '--Please choose an option--'),
            ('missing_items', 'Missing items'),
            ('network', 'Network'),
            ('display_issue', 'Display issue'),
            ('no_issues', 'No issues found'),
            ('unresponsive', 'Unresponsive'),
        ]

        model = KioskCheck
        exclude = ['user']
        fields = [
            'printer', 'reams_used', 'issues', 'toner_status',
            'issue_description', 'ricoh_ticket', 'servicenow_ticket',
            'computer', 'computer_issue',
        ]
        widgets = {
            'reams_used': forms.NumberInput(attrs = {'class': 'form-control', 'min': 0, 'max': 4}),
            'issues': forms.Select(choices = PRINTER_STATUS_CHOICES, attrs = {'class': 'form-control'}),
            'toner_status': forms.Select(choices = TONER_STATUS_CHOICES, attrs = {'class': 'form-control'}),
            'issue_description': forms.Textarea(attrs = {'class': 'form-control'}),
            'ricoh_ticket': forms.TextInput(attrs = {'class': 'form-control'}),
            'servicenow_ticket': forms.TextInput(attrs = {'class': 'form-control'}),
            'computer': forms.TextInput(attrs = {'class': 'form-control'}),
            'computer_issue': forms.Select(choices = COMPUTER_ISSUE_CHOICES, attrs = {'class': 'form-control'}),
        }

    def clean_printer(self):
        data = self.cleaned_data['printer']
        cleaned_data = bleach.clean(data.name, tags=[])
        return cleaned_data

    def clean_issue_description(self):
        data = self.cleaned_data['issue_description']
        allowed_tags = ['b', 'i', 'u', 'a', 'p']
        cleaned_data = bleach.clean(data, tags = allowed_tags)
        return cleaned_data

    def clean_reams_used(self):
        data = self.cleaned_data['reams_used']
        if not (0 <= data <= 4):
            raise forms.ValidationError('Reams Used must be between 0 and 4.')
        return data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    registration_code = forms.CharField(max_length = 20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'registration_code']

    def clean_registration_code(self):
        code = self.cleaned_data.get('registration_code')
        if code != 'HLSITS':
            raise forms.ValidationError('Invalid registration code.')
        return code


class ChargingStationForm(forms.ModelForm):
    class Meta:
        model = ChargingStationCheck
        fields = ['location', 'charger_status', 'issue_description', 'servicenow_ticket']

    CHARGER_STATUS_CHOICES = [
        ('', '--Please choose an option--'),
        ('no_issues', 'No issues found'),
        ('no_charge', 'Does not charge'),
        ('cable-malfunction', 'Cable malfunction'),
    ]

    location = forms.ModelChoiceField(queryset=ChargingStationLocation.objects.all(), label="Charging Station Location", required=True)
    charger_status = forms.ChoiceField(choices=CHARGER_STATUS_CHOICES, label="Charger Status", required=True)
    issue_description = forms.CharField(widget=forms.Textarea, label="Issue Description", required=False)
    servicenow_ticket = forms.CharField(widget=forms.TextInput(attrs={'size': '20'}), required=False)