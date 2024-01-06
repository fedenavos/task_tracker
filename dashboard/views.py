from django.shortcuts import render
from django.db.models import Sum, Count
from tasks.models import Task

def dashboard_view(request):
    # Obtener tareas por estado y calcular totales en una sola consulta por estado
    planned_data = Task.objects.filter(state='Planned').aggregate(
        total_estimate=Sum('estimate'),
        task_count=Count('id')
    )
    in_progress_data = Task.objects.filter(state='In Progress').aggregate(
        total_estimate=Sum('estimate'),
        task_count=Count('id')
    )
    completed_data = Task.objects.filter(state='Completed').aggregate(
        total_estimate=Sum('estimate'),
        task_count=Count('id')
    )

    # Preparar contexto para el template
    context = {
        'planned_tasks': Task.objects.filter(state='Planned').order_by('id'),
        'in_progress_tasks': Task.objects.filter(state='In Progress').order_by('id'),
        'completed_tasks': Task.objects.filter(state='Completed').order_by('id'),
        'total_planned_days': planned_data['total_estimate'] or 0,
        'total_in_progress_days': in_progress_data['total_estimate'] or 0,
        'total_completed_days': completed_data['total_estimate'] or 0,
        'planned_task_count': planned_data['task_count'],
        'in_progress_task_count': in_progress_data['task_count'],
        'completed_task_count': completed_data['task_count'],
    }
    return render(request, 'dashboard/index.html', context)
