from django.db import models


class Recommendation(models.Model):
    mc_username = models.CharField(max_length=16)
    mc_uuid = models.CharField(max_length=36)
    recommendation = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.mc_username
