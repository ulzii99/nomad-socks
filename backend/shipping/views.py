from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShippingZone
from .serializers import ShippingZoneSerializer


class ShippingRatesView(APIView):
    """Get shipping rates for a given country."""

    def get(self, request):
        country = request.query_params.get("country", "MN")
        all_zones = ShippingZone.objects.filter(is_active=True).prefetch_related("rates")

        # Filter zones that include the requested country
        # (done in Python since SQLite doesn't support JSON contains)
        matching = [z for z in all_zones if country in z.countries]

        if not matching:
            # Fall back to international
            matching = [z for z in all_zones if z.name == "International"]

        serializer = ShippingZoneSerializer(matching, many=True)
        return Response(serializer.data)
