from django import template

register = template.Library()

@register.filter
def model_type(instance):
    return type(instance).__name__

@register.filter
def is_null(instance):
    return instance.image is None

@register.simple_tag(takes_context=True)
def show_creator(context, user):
    if user == context['user'].username:
        return "Vous avez"
    else:
        return f"{user} a"

@register.filter
def show_create_review_button(ticket):
    return not ticket.review.all()

@register.simple_tag()
def show_stars(rating):
    if rating == 1:
        return  '★☆☆☆☆'
    elif rating == 2:
        return '★★☆☆☆'
    elif rating == 3:
        return '★★★☆☆'
    elif rating == 4:
        return '★★★★☆'
    elif rating == 5:
        return '★★★★★'
    else:
        return '☆☆☆☆☆'

