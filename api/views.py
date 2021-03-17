from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.utils import json

from recipes.models import (FollowRecipe, FollowUser, Ingredients, Recipe,
                            ShopingList)


SUCCESS_RESPONSE = JsonResponse({'success': True})
BAD_RESPONSE = JsonResponse(
        {'success': False}, status=400
    )

class Ingredient(LoginRequiredMixin, View):
    def get(self, request):
        text = request.GET['query']
        ingredients = list(Ingredients.objects.filter(
            title__icontains=text).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)


class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        req = json.loads(request.body)
        recipe_id = req.get('id', None)
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = FollowRecipe.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                return SUCCESS_RESPONSE
            return JsonResponse({'success': False})
        return BAD_RESPONSE

    def delete(self, request, recipe_id):
        deleted_favourite = FollowRecipe.objects.filter(
            recipe=recipe_id, user=request.user
        ).delete()
        return SUCCESS_RESPONSE


class Subscribe(LoginRequiredMixin, View):
    def post(self, request):
        req = json.loads(request.body)
        author_id = req.get('id', None)
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            obj, created = FollowUser.objects.get_or_create(
                user=request.user, author=author
            )
            if created:
                return SUCCESS_RESPONSE
            return JsonResponse({'success': False})
        return BAD_RESPONSE

    def delete(self, request, author_id):
        deleted_subscription = FollowUser.objects.filter(
            user__username=request.user.username,
            author__id=author_id).delete()
        return SUCCESS_RESPONSE


class Purchase(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShopingList.objects.get_or_create(user=request.user, recipe=recipe)
        return SUCCESS_RESPONSE

    def delete(self, request, recipe_id):
        deleted_purchase = ShopingList.objects.filter(
            user__username=request.user.username,
            recipe__id=recipe_id).delete()
        return SUCCESS_RESPONSE
