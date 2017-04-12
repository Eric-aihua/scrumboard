# encoding:utf-8
import django_filters
from django.contrib.auth import get_user_model

from board.models import Task, Sprint

__author__ = 'eric.sun'


class NullFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name:value})
        return qs


User=get_user_model()

class TaskFilter(django_filters.FilterSet):
    #添加sprint为空的检测过滤:http://localhost:8000/api/tasks/?backlog=True
    backlog=NullFilter(name='sprint')
    class Meta:
        model=Task
        fields=('sprint','status','assigned','backlog')

    def __init__(self,*args,**kwargs):
        super(TaskFilter,self).__init__(*args,**kwargs)
        # 实现对assigned的username 过滤，而不是user_id
        self.filters['assigned'].extra.update({'to_field_name':User.USERNAME_FIELD})


class SprintFilter(django_filters.FilterSet):
    end_min = django_filters.DateFilter(name="end", lookup_expr='gte')
    end_max = django_filters.DateFilter(name="end", lookup_expr='lte')

    class Meta:
        model = Sprint
        fields = ['end_min', 'end_max', ]