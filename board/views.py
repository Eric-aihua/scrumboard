# encoding:utf-8

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import authentication
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from board.models import Sprint, Task
from board.scrum_filters import TaskFilter, SprintFilter
from board.serializer import SprintSerializer, TaskSerializer, UserSerializer


class DefaultMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication, authentication.TokenAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class SprintViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    search_fields = ('name',)
    ordering_fields = ('end', 'name',)
    # Sprint 周期期间的查询
    filter_class=SprintFilter


class TaskViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # 可以通过http://localhost:8000/api/tasks/?search=ddd 的方式进行搜索
    search_fields = ('name', 'description')
    # 排序过滤
    ordering_fields = ('name', 'order', 'started')
    # 关联自定义的filter
    filter_class = TaskFilter


class UserViewSet(DefaultMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD)
