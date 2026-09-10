from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdmin, IsAdminOrEmployee
from .models import Order
from .serializers import OrderSerializer, OrderTrackSerializer


class OrderListCreateView(generics.ListCreateAPIView):


    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrEmployee]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
   
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsAdminOrEmployee()]


class OrderTrackView(generics.RetrieveAPIView):
    
 

    queryset = Order.objects.all()
    serializer_class = OrderTrackSerializer
    lookup_field = 'transaction_id'
    lookup_url_kwarg = 'transaction_id'
    permission_classes = [AllowAny]


class SalesSummaryView(APIView):
   

    permission_classes = [IsAdminOrEmployee]

    def get(self, request):
        now = timezone.localtime()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())

        base_qs = Order.objects.exclude(status=Order.STATUS_CANCELLED)
        daily_qs = base_qs.filter(created_at__gte=today_start)
        weekly_qs = base_qs.filter(created_at__gte=week_start)

        return Response({
            'daily_total': daily_qs.aggregate(total=Sum('total_amount'))['total'] or 0,
            'daily_order_count': daily_qs.count(),
            'weekly_total': weekly_qs.aggregate(total=Sum('total_amount'))['total'] or 0,
            'weekly_order_count': weekly_qs.count(),
        })
