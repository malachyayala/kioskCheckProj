from django.db import models
from django.contrib.auth.models import User


class KioskCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    printer = models.CharField(max_length=100)
    reams_used = models.IntegerField()
    issues = models.CharField(max_length=100)
    toner_status = models.CharField(max_length=50)
    issue_description = models.TextField(blank=True, null=True)
    ricoh_ticket = models.CharField(max_length=50, blank=True, null=True)
    servicenow_ticket = models.CharField(max_length=50, blank=True, null=True)
    completed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.printer} - {self.issues}"
