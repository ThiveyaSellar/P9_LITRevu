from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blog.forms import TicketForm, ReviewForm, FollowerForm
from blog.models import Ticket, Review, UserFollows

@login_required
def home(request):

    # Récupérer tickets
    # Récupérer les tickets et les reviews
    # Récupérer les tickets sans critiques
    # Récupérer les tickets les tickets avec critiques
    # Récupérer les critiques
    # Trier

    # 'tickets_with_reviews': tickets_with_reviews
    # 'tickets_without_reviews': tickets_without_reviews

    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {
        'tickets_and_reviews': tickets_and_reviews,
    }
    return render(request, 'blog/home.html', context=context)

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

@login_required
def create_review_to_ticket(request, id):
    # Récupérer le ticket avec l'id qui a été passé dans l'url
    ticket = Ticket.objects.get(id=id)
    # Créer le formulaire pour la critique
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # Associer le ticket à cette critique
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        review_form = ReviewForm()

    context = {
        'ticket': ticket,
        'review_form': review_form
    }
    return render(request,'blog/create_review_to_ticket.html', context=context)

@login_required
def edit_review(request, id):
    # Récupérer l'id de la critique.
    review = Review.objects.get(id=id)
    if request.method == 'POST' and request.user == review.user:
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('home')
    else:
        review_form = ReviewForm(instance=review)
    return render(request,'blog/edit_review.html', context={'review_form':review_form})

@login_required
def edit_ticket(request, id):
    # Récupérer l'id du ticket
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST' and request.user == ticket.user:
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect('home')
    else:
        ticket_form = TicketForm(instance=ticket)
    return render(request, 'blog/edit_ticket.html', context={'ticket_form':ticket_form})

@login_required
def delete_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST' and request.user == ticket.user:
        ticket.delete()
        return redirect('home')
    return render(request, 'blog/delete_ticket.html', context={'ticket':ticket})

@login_required
def delete_review(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST' and request.user == review.user:
        review.delete()
        return redirect('home')
    return render(request, 'blog/delete_review.html', context={'review':review})

"""@login_required
def followers_list(request):
    # Abonnements :
    # Les lignes où dans la colonne user on a le user courant
    #following = UserFollows.objects.get(user=request.user.id)
    # Abonnés :
    # Les lignes où l'utilisateur courant est dans la colonne followed_user
    #followed_by = UserFollows.objects.all(followed_user=request.user.id)

    #Lister les abonnements puis les abonnées
    if request.method == 'POST':
        form = FollowerForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            # Rester sur la même page
            return redirect('followers-list')
    else:
        form = FollowerForm()

    context = {
        'following': following,
        'followed_by': followed_by,
        'form': form
    }

    return render(request, 'blog/followers.html', context=context)
"""

""""""
@login_required
def followers_list(request):
    # Les utilisateurs que je suis sont mes abonnements
    # Je suis user, ils sont followed_user
    abonnements = UserFollows.objects.filter(user=request.user.id)
    print("-----------------------------------------------------")
    for user in abonnements:
        print(user.followed_user)
    print("-----------------------------------------------------")

    # Les utilisateurs qui me suivent sont les abonnes
    # Je suis suivi je suis followed_user et ils sont user
    abonnes = UserFollows.objects.filter(followed_user=request.user.id)
    for user in abonnes:
        print(user.user)

    #Lister les abonnements puis les abonnées
    '''if request.method == 'POST':
        form = FollowerForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            # Rester sur la même page
            return redirect('followers-list')
    else:
        form = FollowerForm()'''

    context = {
        'abonnements': abonnements,
        'abonnes': abonnes,
        #'form': form
    }

    return render(request, 'blog/followers.html', context=context)
