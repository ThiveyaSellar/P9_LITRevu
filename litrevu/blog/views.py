from itertools import chain

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from blog.forms import TicketForm, ReviewForm, FollowerForm
from blog.models import Ticket, Review, UserFollows
from authentication.models import User


def get_feed_tickets(users, logged_user):
    condition_1 = Q(user__in=users)
    # Exclure les tickets où il est créateur du ticket et de la review
    condition_2 = Q(user=logged_user)
    condition_3 = Q(review__user=logged_user)
    tickets = Ticket.objects.filter(condition_1 & ~(condition_2 & condition_3))
    return tickets


def get_feed_reviews(users, logged_user):
    # Récupérer les critiques des personnes que je suis
    condition_1 = Q(user__in=users)
    # Récupérer les critiques qui portent sur mes tickets
    condition_2 = Q(ticket__user=logged_user)
    reviews = Review.objects.filter(condition_1 | condition_2)
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

    # Récupérer toutes les demandes de critiques avec ces utilisateurs
    tickets = get_feed_tickets(users, request.user)
    reviews = get_feed_reviews(users, request.user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    paginator = Paginator(tickets_and_reviews, 5)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    context = {
        # 'tickets_and_reviews': tickets_and_reviews,
        # devient pour la pagination
        'page_obj': page_obj,
        'page': "home",
        'logged_user': request.user.username
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

    paginator = Paginator(tickets_and_reviews, 5)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    context = {
        # 'tickets_and_reviews': tickets_and_reviews,
        # devient pour la pagination
        'page_obj': page_obj,
        'page': "posts"
    }

    return render(request, 'blog/posts.html', context=context)


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # Ajouter l'utilisateur au ticket
            ticket = form.save(commit=False)
            print(ticket.title)
            print(ticket.image)
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
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
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
    return render(
        request,
        'blog/create_review_to_ticket.html',
        context=context
    )


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
    return render(
        request,
        'blog/edit_review.html',
        context={'ticket': review.ticket, 'review_form': review_form}
    )


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
    return render(
        request,
        'blog/edit_ticket.html',
        context={'ticket_form': ticket_form}
    )


@login_required
def delete_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST' and request.user == ticket.user:
        ticket.delete()
        return redirect('posts')
    return render(
        request,
        'blog/delete_ticket.html',
        context={'ticket': ticket}
    )


@login_required
def delete_review(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST' and request.user == review.user:
        review.delete()
        return redirect('posts')
    return render(
        request,
        'blog/delete_review.html',
        context={'review': review}
    )


'''@login_required
def delete_review(request, id):
    review = Review.objects.get(id=id)
    if str(request.user) == str(review.user):
        print("1")
        review.delete()
    return redirect('posts')
    return render(
    request,
    'blog/delete_review.html',
    context={'review':review}
    )'''


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
            if name == str(request.user):
                message = "Vous ne pouvez pas vous suivre vous même."
            else:
                message = "A voir."
                already_following = False
                for user in abonnements:
                    if name == str(user.followed_user):
                        already_following = True
                        message = f"Vous suivez déjà {name}."
                        break
                if not already_following:
                    print(f"{name} n'est pas suivi")
                # Récupérer l'instance utilisateur avec ce nom
                # following = User.objects.get(username=name)
                # following = get_object_or_404(User, username=name)
                try:
                    following = User.objects.get(username=name)
                    print(following)
                    exists = True
                    if exists and not already_following:
                        relation = UserFollows.objects.create(
                            user=request.user,
                            followed_user=following
                        )
                        relation.save()
                        # Rester sur la même page
                        return redirect('followers-list')
                except User.DoesNotExist:
                    message = f"{name} n'existe pas."

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
