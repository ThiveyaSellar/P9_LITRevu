from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value

from blog.forms import TicketForm, ReviewForm, FollowerForm
from blog.models import Ticket, Review, UserFollows
from authentication.models import User

def get_feed_tickets(users):
    # Si le ticket et la critique ont le même utilisateur
    # Ne pas afficher le ticket
    tickets = Ticket.objects.filter(user__in=users, review__isnull=True)
    # Chercher tous les tickets
    # Chercher tous les tickets qui ont le même utilisateur
    # et qui ont une review avec cette utilisateur
    # Ce que je veux - ce que je ne veux pas

    # Ce que je ne veux pas
    # Tous les tickets qui ont une review
    # Tous les reviews avec un ticket
    #tickets_with_reviews_ids = Review.objects.values('ticket__id')

    # Récupérer les tickets de ces reviews
    #tickets_with_review = Ticket.objects.filter(
     #   id__in=tickets_with_reviews_ids
    #)
    # le créateur du ticket et de la review sont les mêmes

    return tickets

def get_feed_reviews(users):
    reviews = Review.objects.filter(user__in=users)
    return reviews

@login_required
def home(request):

    # Récupérer les relations où l'utilisateur courant est abonné
    relations = UserFollows.objects.filter(user=request.user.id)

    # Récupérer les utilisateurs dans ces relations
    user_names = [request.user.username]
    for relation in relations:
        user_names.append(relation.followed_user)

    users = User.objects.filter(username__in=user_names)

    tickets = get_feed_tickets(users)
    reviews = get_feed_reviews(users)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {
        'tickets_and_reviews': tickets_and_reviews,
        'page': "home"
    }
    return render(request, 'blog/home.html', context=context)

@login_required
def current_user_posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {
        'tickets_and_reviews': tickets_and_reviews,
        'page': "posts"
    }

    return render(request, 'blog/posts.html', context=context)

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
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == "POST":
        if 'ticket_blog' in request.POST:
            ticket_form = TicketForm(request.POST, request.FILES)
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


@login_required
def followers_list(request):
    # Les utilisateurs que je suis sont mes abonnements
    # Je suis user, ils sont followed_user
    abonnements = UserFollows.objects.filter(user=request.user.id)

    # Les utilisateurs qui me suivent sont les abonnes
    # Je suis suivi je suis followed_user et ils sont user
    abonnes = UserFollows.objects.filter(followed_user=request.user.id)

    form = FollowerForm()
    message = ""

    if request.method == 'POST':
        form = FollowerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            print("---------------------")
            print(type(name))
            print(type(request.user))
            if name == str(request.user):
                message = "Vous ne pouvez pas vous suivre vous même."
            else:
                message = "A voir."
                '''# Vérifier si l'abonnement existe déjà
                exists = False
                for user in abonnements:
                    if follow.followed_user == user.followed_user:
                        exists = True
                        break
                if exists:
                    message = f"Vous êtes déjà abonné à {follow.followed_user}."
                else:
                    follow.user = request.user
                    follow.save()
                    # Rester sur la même page
                    return redirect('followers-list')'''

    context = {
        'abonnements': abonnements,
        'abonnes': abonnes,
        'form': form,
        'message': message
    }

    return render(request, 'blog/followers.html', context=context)

@login_required
def unfollow(request, id):
    # Dans la table UserFollows supprimer la ligne où :
    # le user courant est user et le followed user a l'id
    relation = UserFollows.objects.get(followed_user=id, user=request.user.id)
    print(id)
    relation.delete()
    return redirect('followers-list')

