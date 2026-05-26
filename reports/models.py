from django.db import models


class IssueReport(models.Model):
    mc_username = models.CharField(max_length=16)
    mc_uuid = models.CharField(max_length=36)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.mc_username} — {self.short_description}"
