from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class KioskCheck(models.Model):
    """
    Model to represent a Kiosk Check entry.

    Each KioskCheck entry records the details of a check performed on a printer,
    including the user who performed the check, the printer's status, issues found,
    and any associated tickets.
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    printer = models.CharField(max_length = 100)
    reams_used = models.IntegerField()
    issues = models.CharField(max_length = 100)
    toner_status = models.CharField(max_length = 50)
    issue_description = models.TextField(blank = True, null = True)
    ricoh_ticket = models.CharField(max_length = 50, blank = True, null = True)
    servicenow_ticket = models.CharField(max_length = 50, blank = True, null = True)
    completed_date = models.DateTimeField(auto_now_add = True)
    charging_station = models.CharField(max_length = 100, blank = True, null = True)
    computer = models.CharField(max_length = 100, blank = True, null = True)

    def __str__(self):
        """
        String representation of the KioskCheck instance.

        Returns the printer and issues as a string.
        """
        return f"{self.printer} - {self.issues}"
