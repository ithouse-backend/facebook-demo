from django.shortcuts import render, redirect
from .models import Story
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from apps.authentication.models import Friendship


def create_story(request):
    stories = Story.objects.all()
    if request.method == 'POST':
        user = request.user
        file = request.FILES.get("story__file")
        if file:
            Story.objects.create(user=user, image=file)
            messages.success(request, "Your story is successfully uploaded")
            return redirect("/")
        else:
            messages.error(request, "File is required!"),
    context = {
        'stories': stories
    }
    return render(request, 'home/create_story.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def story_detail(request, storyID):
    if is_ajax(request=request):
        print("ajax")
        try:
            story = Story.objects.get(id=storyID)
            if Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user)):
                for user in Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user)):
                    m_stories = Story.objects.filter(
                        user=request.user)  # mening storyim
                    o_stories = Story.objects.exclude(id__in=m_stories.values_list("id", flat=True)).filter(
                        Q(user=user.user1) |
                        Q(user=user.user2)
                    ).order_by("created_at")

                    stories = list(m_stories) + list(o_stories)
                    story_ids = [st.id for st in stories]
                    # Remove the current story ID from the list
                    story_ids = [id for id in story_ids if id != story.id]
                    next_story_id = story_ids[0] if story_ids else None

                    if not story_ids:
                        return JsonResponse({'next_story_id': None})
        except Story.DoesNotExist:
            return JsonResponse({'next_story_id': None})

        return JsonResponse({'next_story_id': next_story_id})
    else:
        story = Story.objects.get(id=storyID)
        print('sefdsd')
        context = {
            "story": story
        }
        return render(request, 'includes/story_content.html', context)
