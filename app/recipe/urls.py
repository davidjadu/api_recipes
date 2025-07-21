from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipe')

app_name = "recipe"  # This is for the reverse mapping

urlpatterns = [path('', include(router.urls))]
