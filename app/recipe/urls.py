from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# defaultrouter feature will automatically register the approprate urls for
# all of the actions in our viewset
# e.g. multiple urls associated with one viewset:
#   /api/recipe/tags
#   /api/recipe/tags/1
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    # pass all requests in our route urls
    path('', include(router.urls))
]
