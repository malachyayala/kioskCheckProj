from django.contrib import admin
from .models import PrinterLocation, ChargingStationLocation

admin.site.register(PrinterLocation)
admin.site.register(ChargingStationLocation)