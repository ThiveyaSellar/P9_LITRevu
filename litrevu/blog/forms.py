from django import forms
from django.contrib.auth import get_user_model
from blog.models import Ticket, Review, UserFollows

User = get_user_model()

class TicketForm(forms.ModelForm):
    ticket_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['size'] = 100
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['description'].widget.attrs['cols'] = 102

    class Meta:
        model = Ticket
        exclude = ('user',)
        labels = {
            "title": "Titre"
        }


class ReviewForm(forms.ModelForm):
    review_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs['size'] = 100
        self.fields['body'].widget.attrs['size'] = 100
        self.fields['body'].widget.attrs['rows'] = 5
        self.fields['body'].widget.attrs['cols'] = 102

    class Meta:
        model = Review
        exclude = ('ticket', 'user', 'time_created')
        fields = ['headline', 'rating', 'body']
        labels = {
            "headline": "Titre",
            "rating": "Note",
            "body": "Commentaire"
        }
        '''widgets = {
            'rating': forms.RadioSelect(
                choices=(
                    (0, '0'),
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5')
                )
            ),
        }'''

class FollowerForm(forms.Form):

    name = forms.CharField(max_length=100, label="Nom d'utilisateur")
    '''class Meta:
        model = UserFollows
        fields = ['followed_user']
'''