from django.shortcuts import render, redirect
from .models import Story
from django.contrib import messages


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


def story_detail(request, storyID):
    story = Story.objects.get(id=storyID)
    context = {
        "story": story
    }
    return render(request, "includes/story_content.html", context)
