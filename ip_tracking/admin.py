from django.contrib import admin
from .models import RequestLog, BlockedIP, SuspiciousIP

admin.site.register(RequestLog)
admin.site.register(BlockedIP)
admin.site.register(SuspiciousIP)

# @admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "path", "timestamp", "country", "city")
    search_fields = ("ip_address", "path", "country", "city")
    list_filter = ("timestamp", "country")
