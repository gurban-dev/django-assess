from django.urls import path

from .views import TaskListCreateView

urlpatterns = [
    # .as_view() turns your view class into a standard function
    # and automatically routes incoming web requests (like GET
    # or POST) to the matching method inside that class.
    path("", TaskListCreateView.as_view(), name="task-list-create"),

    # Assessment: add the individual-task route here.
]