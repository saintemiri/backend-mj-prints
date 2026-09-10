from django.urls import path

from .views import OrderDetailView, OrderListCreateView, OrderTrackView, SalesSummaryView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/track/<str:transaction_id>/', OrderTrackView.as_view(), name='order-track'),
    path('sales/summary/', SalesSummaryView.as_view(), name='sales-summary'),
]
