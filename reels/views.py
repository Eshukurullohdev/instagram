from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Reel
from like.models import ReelsLike


class ReelsView(DetailView):
    model = Reel
    context_object_name = "reel"
    pk_url_kwarg = "unique_id"
    template_name = "reels.html"

    def get_object(self, queryset=None):
        reel = None
        if self.pk_url_kwarg is not None and self.pk_url_kwarg in self.kwargs:
            try:
                url_parameterlar = self.kwargs[self.pk_url_kwarg]
                reel = Reel.objects.get(unique_id=url_parameterlar)
            except Reel.DoesNotExist:
                reel = None
        return reel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_reel = Reel.objects.first()
        like = None
        try:
            like = ReelsLike.objects.get(reel=first_reel, user=self.request.user)
        except ReelsLike.DoesNotExist:
            like = None
        try:
            reel = Reel.objects.get(unique_id=self.kwargs.get("unique_id"))
            if reel == first_reel:
                pass
            else:
                first_reel = None
        except Reel.DoesNotExist:
            reel = None
        try:
            left_r = Reel.objects.filter(date_created__lt=Reel.objects.get(unique_id=self.kwargs.get("unique_id")).date_created).first()
            right_r = None
        except Reel.DoesNotExist:
            left_r = None
        try:
            right_r = Reel.objects.filter(date_created__gt=Reel.objects.get(unique_id=self.kwargs.get("unique_id")).date_created).first()
            if right_r == None:
                right_r = Reel.objects.get(unique_id=self.kwargs.get("unique_id"))
        except Reel.DoesNotExist:
            right_r = None
        context["first_reel"] = first_reel
        context["like"] = like
        context["left_r"] = left_r
        context["right_r"] = right_r
        
        return context
