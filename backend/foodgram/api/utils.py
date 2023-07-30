import base64

from django.db.models import Sum
from django.shortcuts import get_object_or_404, HttpResponse
from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.response import Response

from recipes.models import Ingredient, RecipeIngredient


class Base64ImageField(serializers.ImageField):
    """Вспомогательный класс для работы с изображениями."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def create_ingredients(ingredients, recipe):
    """Вспомогательная функция для добавления,
    создания/редактирования рецепта."""
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(Ingredient,
                                               id=ingredient.get('id'))
        amount = ingredient.get('amount')
        ingredient_list.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        )
    RecipeIngredient.objects.bulk_create(ingredient_list)


def create_model_instance(request, instance, serializer_name):
    """Вспомогательная функция для добавления
    рецепта в избранное или список покупок.
    """
    serializer = serializer_name(
        data={'user': request.user.id, 'recipe': instance.id, },
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_model_instance(request, model_name, instance, error_message):
    """Вспомогательная функция для удаления рецепта
    из избранного, и из списка покупок.
    """
    if not model_name.objects.filter(user=request.user,
                                     recipe=instance).exists():
        return Response({'errors': error_message},
                        status=status.HTTP_400_BAD_REQUEST)
    model_name.objects.filter(user=request.user, recipe=instance).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def shopping_cart(self, request):
    """Вспомогательная функция для загрузки списка покупок."""
    ingredients = RecipeIngredient.objects.filter(
        recipe__carts__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(ingredient_amount=Sum('amount'))
    shopping_list = ['Список покупок:\n']
    for ingredient in ingredients:
        name = ingredient['ingredient__name']
        unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['ingredient_amount']
        shopping_list.append(f'\n{name} - {amount}, {unit}')
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = \
        'attachment; filename="shopping_cart.txt"'
    return response
