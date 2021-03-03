from django.urls import path

from . import views

urlpatterns = [
    path('follow/', views.follow_index, name='follow_index'),
    path('cart/', views.cart, name='cart'),
    path('shopping-list/', views.shopping_list, name='shopping-list'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path(
        'new/',
        views.recipe_new,
        name='recipe_new'
    ),
    path('favourites/', views.favourite_index, name='favourite_index'),
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
    path('<username>/<int:recipe_id>/', views.recipe_view, 
        name='recipe_view'),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
]
