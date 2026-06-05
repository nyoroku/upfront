from django import forms
from .models import CandidateProfile


class OnboardingForm(forms.ModelForm):
    """Form for candidate profile setup after registration."""

    class Meta:
        model = CandidateProfile
        fields = ['destination', 'qualification', 'nck_number', 'phone_number', 'profile_photo']
        widgets = {
            'destination': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-slate-600 bg-slate-800 text-white '
                         'focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
            }),
            'qualification': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-slate-600 bg-slate-800 text-white '
                         'focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
            }),
            'nck_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-slate-600 bg-slate-800 text-white '
                         'focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
                'placeholder': 'e.g. NCK/12345/2024',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-slate-600 bg-slate-800 text-white '
                         'focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
                'placeholder': '254XXXXXXXXX',
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 '
                         'file:rounded-lg file:border-0 file:text-sm file:font-semibold '
                         'file:bg-emerald-600 file:text-white hover:file:bg-emerald-700',
            }),
        }
