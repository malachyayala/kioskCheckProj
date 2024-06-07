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
    COMPUTER_ISSUE_CHOICES = [
        ('missing_items', 'Missing items'),
        ('network', 'Network'),
        ('display_issue', 'Display issue'),
        ('all_good', 'All good'),
        ('unresponsive', 'Unresponsive'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    printer = models.CharField(max_length=100)
    reams_used = models.IntegerField()
    issues = models.CharField(max_length=100)
    toner_status = models.CharField(max_length=50)
    issue_description = models.TextField(blank=True, null=True)
    ricoh_ticket = models.CharField(max_length=50, blank=True, null=True)
    servicenow_ticket = models.CharField(max_length=50, blank=True, null=True)
    completed_date = models.DateTimeField(auto_now_add=True)
    computer = models.CharField(max_length=100, blank=True, null=True)
    computer_issue = models.CharField(max_length=20, choices=COMPUTER_ISSUE_CHOICES, blank=True, null=True)

    def __str__(self):
        """
        String representation of the KioskCheck instance.

        Returns the printer and issues as a string.
        """
        return f"{self.printer} - {self.issues}"


class ChargingStationCheck(models.Model):
    CHARGING_STATION_LOCATIONS = [
        ('location1', 'Location 1'),
        ('location2', 'Location 2'),
        ('location3', 'Location 3'),
        ('location4', 'Location 4'),
        ('location5', 'Location 5'),
        ('location6', 'Location 6'),
        ('location7', 'Location 7'),
        ('location8', 'Location 8'),
        ('location9', 'Location 9'),
        ('location10', 'Location 10'),
        ('location11', 'Location 11'),
        ('location12', 'Location 12'),
        ('location13', 'Location 13'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, choices=CHARGING_STATION_LOCATIONS)
    issue_description = models.TextField()
    servicenow_ticket = models.CharField(max_length = 50, blank = True, null = True)
    completed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.location}"