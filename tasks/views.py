from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer

# How does this class-based view know which function must be
# called to handle GET and POST requests?

# Django REST Framework's APIView handles this through HTTP
# method dispatching.

# When a client sends a request to your API, Django routes
# the URL to the appropriate view. DRF then examines the
# HTTP method and calls the corresponding method on your
# class.

# Unlike a function-based view, you do not need to write an
# if statement to check whether the request is GET or POST.

# The method names get and post have special meaning to APIView.

class TaskListCreateView(APIView):
    """List tasks or validate and create one."""

    def get(self, request):
        tasks = Task.objects.all()

        # The keyword argument many=True tells the serializer that it is
        # processing a collection of objects rather than a single instance
        # of the model class.
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Add a method below that handles a request from the client that
# seeks to get one individual task.

# Take into account the program should not stop running if the
# user passes an ID for a task that does not exist.

# The error that must be caught:
# Task.DoesNotExist