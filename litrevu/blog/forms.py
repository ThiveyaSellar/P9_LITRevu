from django import forms
from blog.models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('user',)