from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views import View
from django_filters.rest_framework import (
    CharFilter,
    ChoiceFilter,
    DateTimeFilter,
    DjangoFilterBackend,
    FilterSet,
    NumberFilter,
)
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from tasks.models import *


class TaskFilter(FilterSet):
    priority = CharFilter(lookup_expr="iexact")
    status = ChoiceFilter(choices=STATUS_CHOICES)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "completed",
            "priority",
            "user",
            "status",
        )


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListAPI(APIView):
    def get(self, request):
        tasks = Task.objects.filter(deleted=False, completed=False)
        data = TaskSerializer(tasks, many=True).data
        return Response({"tasks": data})


class HistorySerializer(ModelSerializer):
    class Meta:
        model = History
        fields = (
            "task",
            "old_status",
            "new_status",
            "time",
        )


class HistoryFilter(FilterSet):
    old_status = ChoiceFilter(choices=STATUS_CHOICES)
    new_status = ChoiceFilter(choices=STATUS_CHOICES)
    time = DateTimeFilter(lookup_expr="gte")


class HistoryViewSet(ReadOnlyModelViewSet):

    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HistoryFilter

    def get_queryset(self):
        if "task_pk" in self.kwargs:
            return History.objects.filter(
                task__user=self.request.user,
                task=self.kwargs["task_pk"],
            )
        return History.objects.filter(task__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
