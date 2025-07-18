from __future__ import unicode_literals
import datetime
from django.utils.text import slugify

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import date
#from hr.models import PositionPay

class TaskList(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    scope = models.ForeignKey('project.ScopeOfWork', on_delete=models.CASCADE, null=True, related_name="scopets")
    priority = models.PositiveIntegerField(default='9999', help_text='Priorty')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + self.scope + self.group + self.pk)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Task Lists"

        # Prevents (at the database level) creation of two lists with the same slug in the same group
        unique_together = ("group", "slug")


class Task(models.Model):
    title = models.CharField(max_length=140)
    task_list = models.ForeignKey('TaskList', on_delete=models.CASCADE, null=True)
    created_date = models.DateField(default=timezone.now, blank=True, null=True)
    
    allotted_time = models.DecimalField(max_digits=18, decimal_places=2, default='0.25', blank=True, null=True, help_text='How long would it take')
    team_size     = models.PositiveIntegerField(default='1', help_text='Team size') 
    def ext_hours(self):
        return self.allotted_time * self.team_size
    total_hours = property(ext_hours)
    
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="todo_created_by", on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="todo_assigned_to",
        on_delete=models.CASCADE,
    )
    #position = models.ForeignKey(PositionPay, on_delete=models.CASCADE, null=True, related_name="pos", help_text='Select position')
    note = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField()

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the Tasks's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo:task_detail", kwargs={"task_id": self.id})

    # Auto-set the Task creation / completed date
    def save(self, **kwargs):
        # If Task is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Task, self).save()

    class Meta:
        ordering = ["priority"]


class Comment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todo_comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField(blank=True)

    def snippet(self):
        # Define here rather than in __str__ so we can use it in the admin list_display
        return "{author} - {snippet}...".format(author=self.author, snippet=self.body[:35])

    def __str__(self):
        return self.snippet()
