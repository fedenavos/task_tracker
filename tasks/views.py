from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def total_estimate(self, request):
        state = request.query_params.get('state', None)
        if not state:
            raise ValueError('The state query param is required')
        total = Task.objects.filter(state=state).aggregate(Sum('estimate'))["estimate__sum"] or 0
        return Response({'total_estimate': total})
