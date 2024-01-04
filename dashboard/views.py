from django.shortcuts import render
from tasks.models import Task

def dashboard_view(request):
    planned_tasks = Task.objects.filter(state='Planned').order_by('id')
    in_progress_tasks = Task.objects.filter(state='In Progress').order_by('id')
    completed_tasks = Task.objects.filter(state='Completed').order_by('id')

    # Calcular los totales
    total_planned_days = sum(task.estimate for task in planned_tasks)
    total_in_progress_days = sum(task.estimate for task in in_progress_tasks)
    total_completed_days = sum(task.estimate for task in completed_tasks)

    context = {
        'planned_tasks': planned_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'total_planned_days': total_planned_days,
        'total_in_progress_days': total_in_progress_days,
        'total_completed_days': total_completed_days,
    }
    return render(request, 'dashboard/index.html', context)