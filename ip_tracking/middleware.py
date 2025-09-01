import logging
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import RequestLog, BlockedIP
from ipgeolocation import IpGeoLocation   # Task 2
from django.core.cache import cache

logger = logging.getLogger(__name__)

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geo = IpGeoLocation(api_key="YOUR_API_KEY")  # Replace with real API key

    def __call__(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        now = timezone.now()

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Try caching geolocation lookup
        geo_data = cache.get(f"geo:{ip}")
        if not geo_data:
            try:
                geo_info = self.geo.get_location(ip)
                geo_data = {
                    "country": geo_info.get("country_name", ""),
                    "city": geo_info.get("city", ""),
                }
                cache.set(f"geo:{ip}", geo_data, timeout=86400)  # 24 hours
            except Exception:
                geo_data = {"country": "", "city": ""}

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=now,
            path=path,
            country=geo_data.get("country"),
            city=geo_data.get("city"),
        )

        logger.info(f"Request from {ip} at {now} to {path}")
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
