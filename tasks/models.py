from django.db import models

class Task(models.Model):
    STATE_CHOICES = [('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed')]

    name = models.CharField(max_length=100)
    description = models.TextField()
    estimate = models.IntegerField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Planned')

    def __str__(self):
        return self.name