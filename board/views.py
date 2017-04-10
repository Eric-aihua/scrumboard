from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import viewsets

from board.models import Sprint, Task
from board.serializer import SprintSerializer, TaskSerializer, UserSerializer


class DefaultMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication, authentication.TokenAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class SprintViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer


class TaskViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewSet(DefaultMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
