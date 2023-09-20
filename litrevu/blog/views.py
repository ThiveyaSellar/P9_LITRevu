from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from blog.forms import TicketForm

@login_required
def home(request):
    return render(request, 'blog/home.html')

@login_required
def create_ticket(request):
    form = TicketForm()
    return render(request, 'blog/create_ticket.html', context={'form': form})
