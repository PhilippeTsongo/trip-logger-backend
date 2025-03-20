from django.conf import settings
import requests
from datetime import datetime, timedelta
import requests


def calculate_route(current, pickup, dropoff):
    api_key = settings.OPENROUTESERVICE_API_KEY

    coordinates = [
        [current["lon"], current["lat"]], 
        [pickup["lon"], pickup["lat"]], 
        [dropoff["lon"], dropoff["lat"]]
    ]

    url = settings.OPENROUTERSERVICE_URL
    headers = {
        "Authorization": api_key, 
        "Content-Type": "application/json"
    }

    payload = {"coordinates": coordinates}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        # Check for response errors
        if response.status_code != 200:
            return {"error": response_data.get("error", "Unknown API error")}

        # Ensure the response contains a valid route
        routes = response_data.get("routes")
        if not routes:
            return {"error": "No valid route found. Please check the locations provided."}

        route = routes[0]
        summary = route.get("summary", {})

        # Ensure summary has duration
        total_seconds = summary.get("duration")
        if total_seconds is None:
            return {"error": "Unexpected API response format. Duration not found."}

        total_hours = round(total_seconds / 3600, 2)  # Convert seconds to hours

        route_instructions = route.get("segments", [{}])[0].get("steps", [])
        
        return {
            "route_instructions": route_instructions,
            "total_trip_hours": total_hours
        }

    except requests.RequestException as e:
        return {"error": f"Failed to connect to OpenRouteService: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
    
def generate_log_sheets(current_cycle_hours, total_trip_hours):
    max_daily_hours = 11  # Maximum allowed driving hours per day
    rest_hours_per_day = 10  # Required rest time after driving limit is reached
    log_sheets = []

    remaining_hours_today = max_daily_hours - current_cycle_hours
    if remaining_hours_today <= 0:
        return [{"message": "Driver has reached the daily limit."}]

    today = datetime.now()
    trip_hours_remaining = total_trip_hours

    while trip_hours_remaining > 0:
        daily_hours = min(remaining_hours_today, trip_hours_remaining, max_daily_hours)
        log_sheets.append({
            "date": today.strftime("%Y-%m-%d"),
            "driving_hours": daily_hours,
            "rest_hours": rest_hours_per_day if daily_hours == max_daily_hours else (24 - daily_hours),
            "status": "On duty" if daily_hours > 0 else "Rest"
        })

        trip_hours_remaining -= daily_hours
        remaining_hours_today = max_daily_hours  # Reset for next day
        today += timedelta(days=1)  # Move to next day

    return log_sheets



def format_errors(errors):
    """
    Formats the validation errors in a custom format.
    Transforms a list of errors to the desired format: 
    {"field": "Error message"}
    """
    formatted_errors = {}
    for field, error_list in errors.items():
        formatted_errors[field] = error_list[0]  # Only take the first error message
    return formatted_errors