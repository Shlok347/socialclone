from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
fro django.views import generic
from group.models import Group, GroupMember
from . import models

# Create your views here.
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs = {'sluf':self.kwargs.get('slug')})

        try:
            GroupMember.objects.create(user = self.request.user, group = group)
        except IntegrityError:
            message.warning(self.request,'warning already a member!')
        else:
            message.success(self.request, 'you are now a menber')

        return super().get(request,*args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)













#End views here
