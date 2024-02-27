from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_story, name='create_story'),
    path('detail/<int:storyID>/', views.story_detail, name='story_detail'),
    path('story/', views.next_story, name='next_story')
]
