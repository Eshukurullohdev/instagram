from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from subscription.models import Subscription
from django.views.generic.base import View
from django.db.models import Q

from .models import Story, ExtendedStory


class SingleStoryView(DetailView):
    model = Story
    template_name = "story_detail.html"
    context_object_name = "story"
    pk_url_kwarg = "username"

    def get_object(self, queryset=None):
        if self.pk_url_kwarg is not None and self.pk_url_kwarg in self.kwargs:
            try:
                url_parameterlar = self.kwargs[self.pk_url_kwarg]
                story = Story.objects.get(user__username=url_parameterlar)
            except Story.DoesNotExist:
                story = None
        return story

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all stories and order them by creation date (newer first)
        current_story = self.get_object()
        file_extension = current_story.resource.name.split(".")[-1]
        all_stories = Story.objects.all().order_by("-date_created")
        all_stories_file_extension = []
        joriy_user = self.request.user
        dost = Subscription.objects.filter(Q(user=joriy_user) | Q(to=joriy_user))
        all_stories = all_stories.filter(
            Q(user__in=dost.values_list("to", flat=True))
            | Q(user__in=dost.values_list("user", flat=True))
            | Q(user=joriy_user)
        ).order_by("-date_created")
        for story in all_stories:
            all_stories_file_extension.append(story.resource.name.split(".")[-1])
        # left story
        right_stories = all_stories.filter(date_created__lt=current_story.date_created)
        context["right_stories"] = right_stories
        context["all_stories"] = zip(all_stories, all_stories_file_extension)
        my_extended_story = ExtendedStory.objects.filter(story=current_story)
        context["total_story_count"] = range(0, len(my_extended_story) + 1)
        print(my_extended_story)
        if (
            file_extension == "jpg"
            or file_extension == "png"
            or file_extension == "jpeg"
        ):
            context["file_extension"] = "rasm"
        elif file_extension == "mp4":
            context["file_extension"] = "video"
        return context


class CreateStoryView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "create_story.html")


class CreateStoryWithResource(View):
    def get(self, request, *args, **kwargs):
        return render(request, "create_story_with_image.html")

    def post(self, request, *args, **kwargs):
        story_image = request.FILES.get("story_image")
        try:
            story = Story.objects.get(user=request.user)
            if story:
                ExtendedStory.objects.create(
                    story=story, user=request.user, resource=story_image, text="salom"
                )
        except Story.DoesNotExist:
            Story.objects.create(user=request.user, resource=story_image, text="salom")
        return redirect("/")
