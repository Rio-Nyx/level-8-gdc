"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks.apiviews import TaskListAPI
from rest_framework.routers import SimpleRouter
from tasks.apiviews import TaskViewSet, HistoryViewSet
from rest_framework_nested import routers
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from tasks.views import *
from tasks.reports import GenericReportUpdateView

router = SimpleRouter()
router.register(r"api/task", TaskViewSet)
api_router = routers.NestedSimpleRouter(router, "api/task", lookup="history")
api_router.register(r"history", HistoryViewSet)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("taskapi", TaskListAPI.as_view()),
        path("", GenericTaskView.as_view()),
        path("user/login", UserLoginView.as_view()),
        path("user/signup", UserCreateView.as_view()),
        path("user/logout", LogoutView.as_view()),
        path("tasks", GenericTaskView.as_view()),
        path("create-task", GenericTaskCreateView.as_view()),
        path("update-task/<pk>", GenericTaskUpdateView.as_view()),
        path("delete-task/<pk>", GenericTaskDeleteView.as_view()),
        path("report", GenericReportUpdateView.as_view()),
    ]
    + router.urls
    + api_router.urls
)
