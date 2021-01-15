from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

class Summary(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summary_summary')

    def get_absolute_url(self):
        return reverse('summary:summary_detail', kwargs={'pk': self.pk})
