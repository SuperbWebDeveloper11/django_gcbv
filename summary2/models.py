from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Summary(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summary2_summary')

    def get_absolute_url(self):
        return reverse('summary2:summary_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summary2_comments')
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, related_name='comments')

