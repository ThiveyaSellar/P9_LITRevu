"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', blog.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path(
        'tickets/add-ticket/',
        blog.views.create_ticket,
        name='create-ticket'
    ),
    path(
        'tickets/add-review/',
        blog.views.create_review,
        name='create-review'
    ),
    path(
        'tickets/add-review-to-ticket/<int:id>/',
        blog.views.create_review_to_ticket,
        name='create-review-to-ticket'
    ),
    path(
        'tickets/edit-ticket/<int:id>',
        blog.views.edit_ticket,
        name='edit-ticket'
    ),
    path(
        'tickets/edit_review/<int:id>',
        blog.views.edit_review,
        name='edit-review'
    ),
    path(
        'tickets/delete_ticket/<int:id>',
        blog.views.delete_ticket,
        name='delete-ticket'
    ),
    path(
        'tickets/delete_review/<int:id>',
        blog.views.delete_review,
        name='delete-review'
    ),
    path(
        'followers/',
        blog.views.followers_list,
        name='followers-list'
    ),
    path(
        'followers/delete/<int:id>',
        blog.views.unfollow,
        name='unfollow'
    ),
    path(
        'posts/',
        blog.views.current_user_posts,
        name='posts'
    )
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
