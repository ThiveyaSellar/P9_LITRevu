from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blog.forms import TicketForm, ReviewForm

@login_required
def home(request):
    return render(request, 'blog/home.html')

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            # Ajouter l'utilisateur au ticket
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    else:
        form = TicketForm()
    return render(request, 'blog/create_ticket.html', context={'form': form})

@login_required
def create_review(request):
    if request.method == "POST":
        if 'ticket_blog' in request.POST:
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid():
                # Ajouter l'utilisateur au ticket
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                if 'review_blog' in request.POST:
                    review_form = ReviewForm(request.POST)
                    if review_form.is_valid():
                        review = review_form.save(commit=False)
                        review.ticket = ticket
                        review.user = request.user
                        review.save()
                        return redirect('home')
    else:
        ticket_form = TicketForm()
        review_form  = ReviewForm()
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(request, 'blog/create_review.html', context=context)
