from django import forms
from django.contrib.auth import get_user_model
from blog.models import Ticket, Review, UserFollows

User = get_user_model()

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

class FollowerForm(forms.Form):

    name = forms.CharField(max_length=100)
    '''class Meta:
        model = UserFollows
        fields = ['followed_user']
'''