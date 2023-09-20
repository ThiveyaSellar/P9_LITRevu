from django import forms
from blog.models import Ticket, Review

class TicketForm(forms.ModelForm):
    ticket_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        exclude = ('user',)

class ReviewForm(forms.ModelForm):
    review_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Review
        exclude = ('ticket', 'user', 'time_created')
        fields = ['headline', 'rating', 'body']

