from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.exceptions import ValidationError
from .serializers import TripSerializer, TripSerializerList
from .utils import calculate_route, generate_log_sheets,  format_errors
from .models import Trip
import json

class TripListCreateAPIView(APIView):
    """
    View to list all trips and create a new trip.
    """

    def get(self, request, *args, **kwargs):
        try:
            trips = Trip.objects.all().order_by('-created_at')  # Fetch all trips from the database
            
            serializer = TripSerializerList(trips, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred. Please try again later {str(e)} "}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, *args, **kwargs):
        try:
            serializer = TripSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": format_errors(serializer.errors)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = serializer.validated_data

            # Get route details, including total trip hours
            route_data = calculate_route(
                {"lat": data["current_location"]["lat"], "lon": data["current_location"]["lon"]},
                {"lat": data["pickup_location"]["lat"], "lon": data["pickup_location"]["lon"]},
                {"lat": data["dropoff_location"]["lat"], "lon": data["dropoff_location"]["lon"]}
            )

            if "error" in route_data:
                return Response({"error": route_data["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # Use the total trip hours from route_data
            total_trip_hours = route_data.get("total_trip_hours", 0)  # Default to 0 if missing

            log_sheets = generate_log_sheets(data["current_cycle_hours"], total_trip_hours=total_trip_hours)

            # save the trip data to the database
            trip = Trip.objects.create(
                current_location=data["current_location"],
                pickup_location=data["pickup_location"],
                dropoff_location=data["dropoff_location"],
                current_cycle_hours=data["current_cycle_hours"]
            )

            return Response(
                {
                    "route_instructions": route_data["route_instructions"],
                    "log_sheet": log_sheets,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred. Please try again later. {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TripDetailAPIView(APIView):
    """
    View to details of a trip.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            trip = Trip.objects.get(id=pk)

            serializer = TripSerializerList(trip)
            current_location_dict = json.loads(serializer.data['current_location'].replace("'", '"'))  # Ensure it's valid JSON
            pickup_location_dict = json.loads(serializer.data['pickup_location'].replace("'", '"'))  # Ensure it's valid JSON
            dropoff_location_dict = json.loads(serializer.data['dropoff_location'].replace("'", '"'))  # Ensure it's valid JSON
            current_cycle_hours = serializer.data['current_cycle_hours']
            
            # # Get route details, including total trip hours
            route_data = calculate_route(
                {"lat": current_location_dict.get('lat', None), "lon": current_location_dict.get('lon', None)},
                {"lat": pickup_location_dict.get('lat', None), "lon": pickup_location_dict.get('lon', None)},
                {"lat": dropoff_location_dict.get('lat', None), "lon": dropoff_location_dict.get('lon', None)},
            )

            if "error" in route_data:
                return Response({"error": route_data["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # # Use the total trip hours from route_data
            total_trip_hours = route_data.get("total_trip_hours", 0)  # Default to 0 if missing

            log_sheets = generate_log_sheets(current_cycle_hours, total_trip_hours=total_trip_hours)

            return Response(
                {
                    "data": serializer.data,
                    "route_instructions": route_data["route_instructions"],
                    "log_sheet": log_sheets,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": f"An unexpected error occurred. {str(e)} "}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        