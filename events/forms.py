from django import forms
from .models import Ticket

class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event']
