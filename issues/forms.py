from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', 'image', 'location_address', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded mt-1 bg-white/50 backdrop-blur-sm focus:ring-2 focus:ring-blue-500 outline-none'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded mt-1 bg-white/50 backdrop-blur-sm focus:ring-2 focus:ring-blue-500 outline-none', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded mt-1 bg-white/50 backdrop-blur-sm focus:ring-2 focus:ring-blue-500 outline-none'}),
            'image': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded mt-1 bg-white/50 backdrop-blur-sm'}),
            'location_address': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded mt-1 bg-white/50 backdrop-blur-sm focus:ring-2 focus:ring-blue-500 outline-none', 'placeholder': 'Enter street name or landmark'}),
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('latitude')
        lng = cleaned_data.get('longitude')
        address = cleaned_data.get('location_address')

        if not (lat and lng) and not address:
            raise forms.ValidationError("Please provide either a Map Location or a Manual Address.")
        
        return cleaned_data
