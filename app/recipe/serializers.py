"""
Serializers for the recipe API.
"""

from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
            'tags',
            'ingredients'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new recipe with associated tags and ingredients."""
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags_data, recipe)
        self._get_or_create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe and its associated tags."""
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)

        if tags_data is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags_data, instance)

        if ingredients_data is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients_data, instance)

        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()

        return instance

    def _get_or_create_tags(self, tags_data, instance):
        auth_user = self.context['request'].user
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(user=auth_user, **tag_data)
            instance.tags.add(tag)

    def _get_or_create_ingredients(self, ingredients_data, instance):
        auth_user = self.context['request'].user
        for ingredient_data in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(
                user=auth_user, **ingredient_data)
            instance.ingredients.add(ingredient)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for detailed recipe objects."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
        read_only_fields = RecipeSerializer.Meta.read_only_fields
