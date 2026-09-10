from django import forms
from django.utils import timezone
from booking.models import Booking

class BookingForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional comment'})
    )

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'comment']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def clean(self):
        clean_data = super().clean()
        today = timezone.localdate()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("Start date must be before end date.")
        if start_date < today:
            raise forms.ValidationError("Start date must be before today.")
        return clean_data