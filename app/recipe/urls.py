from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipe')
router.register('tags', views.TagViewSet, basename='tag')
router.register('ingredients', views.IngredientViewSet, basename='ingredient')

app_name = "recipe"  # This is for the reverse mapping

urlpatterns = [path('', include(router.urls))]
