from django.urls import path

from .views import EmployeeListCreateView, LoginView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
]
