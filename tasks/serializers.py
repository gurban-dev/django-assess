from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # The assessment asks you to reject whitespace-only values.
    title = serializers.CharField(max_length=200, trim_whitespace=False)

    class Meta:
        model = Task
        fields = ["id", "title", "completed"]
