from django.urls import path
from .views import TripListCreateAPIView, TripDetailAPIView

urlpatterns = [
    path('trip', TripListCreateAPIView.as_view(), name='trip-create-list-api'),
    path('trip/<str:pk>', TripDetailAPIView.as_view(), name='trip-detail-api'),
]
